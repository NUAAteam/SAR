document.addEventListener('DOMContentLoaded', function() {
    const targetImage = document.getElementById('target-image');
    const interactionLayer = document.getElementById('interaction-layer');
    const selectedCoordinates = document.getElementById('selected-coordinates');
    const startSimulationButton = document.getElementById('start-simulation');
    const resultImage = document.getElementById('result-image');
    const simulationResults = document.getElementById('simulation-results');

    let selectedX = null;
    let selectedY = null;
    let originalImageWidth = null;
    let originalImageHeight = null;

    // 从 URL 参数获取选中的图片名称
    const urlParams = new URLSearchParams(window.location.search);
    const selectedImageName = urlParams.get('image');
    console.log('Selected Image Name:', selectedImageName);

    if (selectedImageName) {
        const selectedImageDataURL = localStorage.getItem(selectedImageName);
        console.log('Image Data URL exists:', !!selectedImageDataURL);

        if (selectedImageDataURL) {
            const img = new Image();
            img.onload = function() {
                originalImageWidth = img.width;
                originalImageHeight = img.height;
                targetImage.src = selectedImageDataURL;
                updateInteractionLayer();
            };
            img.src = selectedImageDataURL;
        } else {
            console.error('No image data found for:', selectedImageName);
            alert('无法加载图片数据，请返回上一页重新选择图片。');
        }
    } else {
        console.error('No selected image name found in URL parameters');
        alert('未选择图片，请返回上一页选择图片。');
    }

    function updateInteractionLayer() {
        interactionLayer.width = targetImage.width;
        interactionLayer.height = targetImage.height;
    }

    targetImage.addEventListener('load', updateInteractionLayer);

    function handleImageClick(e) {
        const rect = interactionLayer.getBoundingClientRect();
        const scaleX = originalImageWidth / rect.width;
        const scaleY = originalImageHeight / rect.height;

        selectedX = Math.round((e.clientX - rect.left) * scaleX);
        selectedY = Math.round((e.clientY - rect.top) * scaleY);

        selectedCoordinates.textContent = `(${selectedX}, ${selectedY})`;

        // 在画布上标记选中的点
        const ctx = interactionLayer.getContext('2d');
        ctx.clearRect(0, 0, interactionLayer.width, interactionLayer.height);
        ctx.fillStyle = 'red';
        ctx.beginPath();
        ctx.arc(e.clientX - rect.left, e.clientY - rect.top, 5, 0, 2 * Math.PI);
        ctx.fill();
    }

    interactionLayer.addEventListener('click', handleImageClick);

    startSimulationButton.addEventListener('click', async function() {
        if (selectedX === null || selectedY === null) {
            alert('请先选择坐标');
            return;
        }

        const selectedImageDataURL = localStorage.getItem(selectedImageName);
        if (!selectedImageDataURL) {
            alert('图片数据不存在，请返回上一页重新选择图片。');
            return;
        }

        const formData = new FormData();
        formData.append('image', dataURLtoBlob(selectedImageDataURL), selectedImageName);
        formData.append('b', document.getElementById('b').value);
        formData.append('threshold', document.getElementById('threshold').value);
        formData.append('x', selectedX.toString());
        formData.append('y', selectedY.toString());

        try {
            const response = await fetch('http://localhost:5000/sar_simulate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.image) {
                resultImage.src = 'data:image/png;base64,' + data.image;
                simulationResults.style.display = 'block';
            } else {
                throw new Error('No image data in response');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('仿真失败: ' + error.message);
        }
    });

    function dataURLtoBlob(dataURL) {
        if (!dataURL) {
            throw new Error('dataURL is null or undefined');
        }
        const arr = dataURL.split(',');
        const mime = arr[0].match(/:(.*?);/)[1];
        const bstr = atob(arr[1]);
        let n = bstr.length;
        const u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], {type: mime});
    }
});