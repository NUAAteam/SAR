const cv = require('opencv4nodejs');
const fs = require('fs');
const path = require('path');
const { createCanvas, loadImage } = require('canvas');
const { noise2D } = require('perlin-noise');
const { JSDOM } = require('jsdom');
const { ChartJSNodeCanvas } = require('chartjs-node-canvas');
const { randomNormal } = require('d3-random');

class Point {
    constructor(i, j, ic, jc, k, sigma) {
        this.i = i;
        this.j = j;
        this.ic = ic;
        this.jc = jc;
        this.k = k;
        this.sigma = sigma;
    }

    dist() {
        return Math.sqrt((this.i - this.ic) ** 2 + (this.j - this.jc) ** 2);
    }

    pab() {
        return Math.exp(-this.dist() ** 2 / (this.k * this.sigma));
    }

    status() {
        return 1 - Math.floor(Math.random() + 1 - this.pab());
    }

    area() {
        return randomNormal(this.dist(), this.sigma)();
    }

    gray() {
        return this.dist() !== 0 ? Math.floor(150 * this.sigma ** 2 / this.dist()) : 1024;
    }
}

function process(i, j, ic, jc, k, sigma, picture) {
    const p = new Point(i, j, ic, jc, k, sigma);
    if (p.status() === 1) {
        let area = p.area();
        if (area <= 0) area = 0.0001;
        const a = randomNormal(Math.sqrt(area), p.sigma * 0.5)();

        const x1 = i - a / 2, y1 = j - a / 2;
        const x2 = i + a / 2, y2 = j - a / 2;
        const x3 = i + a / 2, y3 = j + a / 2;
        const x4 = i - a / 2, y4 = j + a / 2;

        const rr = [y1, y2, y3, y4, y1].map(y => Math.round(y)).filter(y => y >= 0 && y < picture.rows);
        const cc = [x1, x2, x3, x4, x1].map(x => Math.round(x)).filter(x => x >= 0 && x < picture.cols);

        if (rr.length < 4 || cc.length < 4) return;

        const grayPic = picture.getRegion(new cv.Rect(cc[0], rr[0], cc[2] - cc[0], rr[2] - rr[0]));
        const temp1 = cv.subtract(grayPic, new cv.Mat(grayPic.rows, grayPic.cols, cv.CV_8U, p.gray()));
        const temp2 = cv.add(grayPic, new cv.Mat(grayPic.rows, grayPic.cols, cv.CV_8U, p.gray()));

        const m = cv.min(temp1, temp2);
        const n = cv.max(temp1, temp2);

        const ratio = 2;
        const grayValue = cv.Mat.zeros(grayPic.rows, grayPic.cols, cv.CV_8U);
        grayValue.forEach((val, row, col) => {
            grayValue.set(row, col, Math.floor(Math.random() * (n.at(row, col) - m.at(row, col)) + m.at(row, col)));
        });

        grayPic.copyTo(picture.getRegion(new cv.Rect(cc[0], rr[0], cc[2] - cc[0], rr[2] - rr[0])));
    }
}

function processPicture(dm, dn, ic, jc, k, sigma, picture) {
    const startI = Math.max(ic - 250, 0);
    const endI = Math.min(ic + 250, picture.cols);
    const startJ = Math.max(jc - 250, 0);
    const endJ = Math.min(jc + 250, picture.rows);

    for (let i = startI; i < endI; i += dn) {
        for (let j = startJ; j < endJ; j += dm) {
            process(i, j, ic, jc, k, sigma, picture);
        }
    }

    return picture;
}

async function simulate(uploadedFilePath, options) {
    const { dm, dn, ic, jc, k, sigma } = options;

    let picture;
    if (uploadedFilePath) {
        picture = await cv.imreadAsync(uploadedFilePath, cv.IMREAD_GRAYSCALE);
    } else {
        const imgPath = path.resolve(__dirname, 'assets', 'nuaa_sar.jpg');
        picture = await cv.imreadAsync(imgPath, cv.IMREAD_GRAYSCALE);
    }

    const processedPicture = processPicture(dm, dn, ic, jc, k, sigma, picture);

    const originalImageBuffer = cv.imencode('.jpg', picture);
    const processedImageBuffer = cv.imencode('.jpg', processedPicture);

    const originalImage = await loadImage(originalImageBuffer);
    const processedImage = await loadImage(processedImageBuffer);

    const width = processedImage.width;
    const height = processedImage.height;

    const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height });

    const config = {
        type: 'line',
        data: {
            labels: Array.from({ length: width }, (_, i) => i),
            datasets: [{
                label: 'Processed Image',
                data: processedImage.data,
                borderColor: 'rgba(255, 0, 0, 1)',
                borderWidth: 1,
                fill: false,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    ticks: {
                        stepSize: 150
                    }
                },
                y: {
                    ticks: {
                        stepSize: 150
                    }
                }
            }
        }
    };

    const chartBuffer = await chartJSNodeCanvas.renderToBuffer(config);

    return { processedPicture, chartBuffer };
}

module.exports = simulate;
