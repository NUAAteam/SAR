const cv = require('opencv4nodejs');
const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');
const path = require('path');
const { fft2, ifft2, fftshift, ifftshift } = require('fft-js');

function regionGrowing(img, seed, threshold) {
    const visited = new Array(img.rows).fill(0).map(() => new Array(img.cols).fill(false));
    const dx = [-1, 0, 1, 0];
    const dy = [0, 1, 0, -1];
    const queue = [[seed.x, seed.y]];
    const seedValue = img.at(seed.y, seed.x);

    while (queue.length > 0) {
        const [x, y] = queue.shift();
        if (visited[y][x]) continue;
        if (Math.abs(img.at(y, x) - seedValue) <= threshold) {
            visited[y][x] = true;
            img.set(y, x, 0);
            for (let i = 0; i < 4; i++) {
                const nx = x + dx[i];
                const ny = y + dy[i];
                if (nx >= 0 && nx < img.cols && ny >= 0 && ny < img.rows && !visited[ny][nx]) {
                    queue.push([nx, ny]);
                }
            }
        }
    }
    return img;
}

function lowPassFilter(image, cutoff) {
    const [rows, cols] = image.sizes;
    const crow = Math.floor(rows / 2);
    const ccol = Math.floor(cols / 2);
    const mask = new cv.Mat(rows, cols, cv.CV_8U, 0);
    mask.getRegion(new cv.Rect(ccol - cutoff, crow - cutoff, cutoff * 2, cutoff * 2)).setTo(255);

    const fshift = fftshift(fft2(image));
    const fshiftMasked = fshift.map((row, i) => row.map((val, j) => val * mask.at(i, j)));
    const imgBack = ifft2(ifftshift(fshiftMasked));

    return imgBack;
}

function sar(filePath, x, y, threshold, b) {
    const img = cv.imread(filePath, cv.IMREAD_GRAYSCALE);

    const seed = { x: parseInt(x), y: parseInt(y) };
    regionGrowing(img, seed, parseInt(threshold));

    const omega = 5.0 * Math.sqrt(img.rows * img.cols) / b;

    const theta = cv.Mat.zeros(img.rows, img.cols, cv.CV_64F).map(() => Math.random() * 2 * Math.PI);
    const complexImg = cv.Mat.zeros(img.rows, img.cols, cv.CV_64F);
    img.convertTo(complexImg, cv.CV_64F);

    const complexImgWithTheta = complexImg.map((val, i, j) => val * Math.exp(1 * j * theta.at(i, j)));
    const filteredImg = lowPassFilter(complexImgWithTheta, parseInt(omega));

    const outputPath = path.join(__dirname, 'results', 'filtered_image.png');
    cv.imwrite(outputPath, cv.Mat.abs(filteredImg));

    return outputPath;
}

module.exports = sar;
