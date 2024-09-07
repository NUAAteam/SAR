document.addEventListener('DOMContentLoaded', function() {
    const targetImage = document.getElementById('target-image');
    const interactionLayer = document.getElementById('interaction-layer');
    const selectedCoordinates = document.getElementById('selected-coordinates');
    const startSimulationButton = document.getElementById('start-simulation');
    const imageRegistration = document.getElementById('image-registration');
    const startRegistrationButton = document.getElementById('start-registration');
    const beforeImage = document.getElementById('before-image');
    const afterImage = document.getElementById('after-image');

    let selectedX = null;
    let selectedY = null;
    let originalImageWidth = null;
    let originalImageHeight = null;
    let originalImageSrc = null;

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
            showMessage('无法加载图片数据，请返回上一页重新选择图片。', 'error');
        }
    } else {
        console.error('No selected image name found in URL parameters');
        showMessage('未选择图片，请返回上一页选择图片。', 'error');
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
            showMessage('请先选择坐标', 'warning');
            return;
        }

        const selectedImageDataURL = localStorage.getItem(selectedImageName);
        if (!selectedImageDataURL) {
            showMessage('图片数据不存在，请返回上一页重新选择图片。', 'error');
            return;
        }

        showMessage('正在进行仿真...', 'info');

        const formData = new FormData();
        formData.append('image', dataURLtoBlob(selectedImageDataURL), selectedImageName);
        formData.append('dm', document.getElementById('dm').value);
        formData.append('dn', document.getElementById('dn').value);
        formData.append('ic', selectedX.toString());
        formData.append('jc', selectedY.toString());
        formData.append('k', document.getElementById('k').value);
        formData.append('sigma', document.getElementById('sigma').value);

        console.log('Sending coordinates:', selectedX, selectedY);

        try {
            const response = await fetch('http://localhost:5000/simulate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.image) {
                originalImageSrc = targetImage.src;  // 保存原始图像
                targetImage.src = 'data:image/png;base64,' + data.image;
                selectedX = null;
                selectedY = null;
                selectedCoordinates.textContent = '未选择';
                const ctx = interactionLayer.getContext('2d');
                ctx.clearRect(0, 0, interactionLayer.width, interactionLayer.height);
                showMessage('仿真完成！您可以在图像上选择新的坐标进行下一次仿真。', 'success');

                // 显示图像配准部分
                imageRegistration.style.display = 'block';

                // 设置仿真前后的图像
                beforeImage.src = originalImageSrc;
                afterImage.src = targetImage.src;
            } else {
                throw new Error('No image data in response');
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('仿真失败: ' + error.message, 'error');
        }
    });

    startRegistrationButton.addEventListener('click', function() {
        document.getElementById('registration-process').style.display = 'block';
        startRegistrationProcess();
    });

    async function startRegistrationProcess() {
        const steps = ['feature-detection', 'feature-matching', 'transform-estimation', 'image-warping'];
        for (let step of steps) {
            document.getElementById(step).classList.add('active');
            await simulateProcessingStep();
            document.getElementById(step).classList.remove('active');
        }
        showRegistrationResult();
    }

    function simulateProcessingStep() {
        return new Promise(resolve => setTimeout(resolve, 1000)); // 模拟处理时间
    }

    function showRegistrationResult() {
        document.getElementById('registration-result').style.display = 'block';
        const resultComparison = document.getElementById('result-comparison');
        resultComparison.innerHTML = `
            <img src="${afterImage.src}" alt="配准结果">
            <div class="comparison-slider"></div>
        `;
        initComparisonSlider();
    }

    function initComparisonSlider() {
        const resultComparison = document.getElementById('result-comparison');
        let slider = resultComparison.querySelector('.comparison-slider');
        let isResizing = false;
        let sliderPosition = 0.5; // 初始位置在中间

        // 确保两张图片都已加载
        const beforeImage = document.getElementById('before-image');
        const afterImage = document.getElementById('after-image');

        resultComparison.innerHTML = `
            <img src="${beforeImage.src}" alt="仿真前图像" class="before-image">
            <img src="${afterImage.src}" alt="仿真后图像" class="after-image">
            <div class="comparison-slider"></div>
            <p class="slider-instruction">拖动滑块或使用鼠标滚轮来比较仿真前后的图像</p>
        `;

        // 重新获取slider元素，因为我们刚刚重新创建了DOM
        slider = resultComparison.querySelector('.comparison-slider');
        const beforeResultImage = resultComparison.querySelector('.before-image');
        const afterResultImage = resultComparison.querySelector('.after-image');

        function updateSliderPosition() {
            slider.style.left = `${sliderPosition * 100}%`;
            afterResultImage.style.clipPath = `inset(0 0 0 ${sliderPosition * 100}%)`;
        }

        function onMouseMove(e) {
            if (!isResizing) return;
            const rect = resultComparison.getBoundingClientRect();
            sliderPosition = (e.clientX - rect.left) / rect.width;
            sliderPosition = Math.max(0, Math.min(sliderPosition, 1));
            updateSliderPosition();
        }

        function onMouseUp() {
            isResizing = false;
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        }

        slider.addEventListener('mousedown', function(e) {
            isResizing = true;
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
            e.preventDefault();
        });

        // 添加鼠标滚轮控制
        resultComparison.addEventListener('wheel', function(e) {
            e.preventDefault();
            const delta = e.deltaY > 0 ? -0.01 : 0.01;
            sliderPosition = Math.max(0, Math.min(sliderPosition + delta, 1));
            updateSliderPosition();
        });

        // 初始化滑块位置
        updateSliderPosition();
    }

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

    function showMessage(message, type) {
        // 如果你想保留 alert，可以使用下面的代码
        // alert(message);

        // 如果你想使用更友好的消息提示，可以使用下面的代码
        const messageContainer = document.getElementById('message-container');
        messageContainer.textContent = message;
        messageContainer.className = `message ${type}`;
        messageContainer.style.display = 'block';
        setTimeout(() => {
            messageContainer.style.display = 'none';
        }, 6000);
    }
});