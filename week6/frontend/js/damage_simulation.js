document.addEventListener('DOMContentLoaded', function() {
    const targetImage = document.getElementById('target-image');
    const interactionLayer = document.getElementById('interaction-layer');
    const selectedCoordinates = document.getElementById('selected-coordinates');
    const startSimulationButton = document.getElementById('start-simulation');
    const imageRegistration = document.getElementById('image-registration');
    const startRegistrationButton = document.getElementById('start-registration');
    const beforeImage = document.getElementById('before-image');
    const afterImage = document.getElementById('after-image');
    const startAssessmentButton = document.getElementById('start-assessment');
    const damageImage = document.getElementById('damage-image');
    const damageStatistics = document.getElementById('damage-statistics');
    const damageLevelSelector = document.getElementById('damage-level');
    const damageDescription = document.getElementById('damage-description');
    const damageCanvas = document.createElement('canvas');
    const damageImageContainer = document.getElementById('damage-image-container');

    let selectedX = null;
    let selectedY = null;
    let originalImageWidth = null;
    let originalImageHeight = null;
    let originalImageSrc = null;
    let simulatedImage = null;
    let damageData = null; // 用于存储毁伤数据

    const damageLevelDescriptions = {
        'all': '显示所有毁伤等级',
        '1': '1级毁伤 (轻微损伤): 目标表面有轻微划痕或凹陷，功能基本不受影响。损伤范围：0-25%',
        '2': '2级毁伤 (中等损伤): 目标表面有明显损坏，部分功能可能受到影响。损伤范围：26-50%',
        '3': '3级毁伤 (严重损伤): 目标结构受到严重破坏，大部分功能丧失。损伤范围：51-75%',
        '4': '4级毁伤 (完全损毁): 目标完全被摧毁，无法修复。损伤范围：76-100%'
    };

    const damageLevelColors = {
        '1': [255, 255, 0, 128],   // 黄色，半透明
        '2': [255, 165, 0, 128],   // 橙色，半透明
        '3': [255, 0, 0, 128],     // 红色，半透明
        '4': [128, 0, 128, 128]    // 紫色，半透明
    };

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
                originalImageSrc = selectedImageDataURL;  // 设置 originalImageSrc
                beforeImage.src = originalImageSrc;  // 确保 beforeImage 显示原始图像
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
                targetImage.src = 'data:image/png;base64,' + data.image;
                simulatedImage = 'data:image/png;base64,' + data.image;
                selectedX = null;
                selectedY = null;
                selectedCoordinates.textContent = '未选择';
                const ctx = interactionLayer.getContext('2d');
                ctx.clearRect(0, 0, interactionLayer.width, interactionLayer.height);
                showMessage('仿真完成！', 'success');
                imageRegistration.style.display = 'block';
                afterImage.src = simulatedImage;  // 设置 afterImage 显示仿真后图像
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
            <img src="${originalImageSrc}" alt="仿真前图像" class="before-image">
            <img src="${afterImage.src}" alt="仿真后图像" class="after-image">
            <div class="comparison-slider"></div>
            <p class="slider-instruction">拖动滑块或使用鼠标滚轮来比较仿真前后的图像</p>
        `;
        initComparisonSlider();

        // 显示毁伤评估按钮
        document.getElementById('damage-assessment').style.display = 'block';
    }

    function initComparisonSlider() {
        const resultComparison = document.getElementById('result-comparison');
        let slider = resultComparison.querySelector('.comparison-slider');
        let isResizing = false;
        let sliderPosition = 0.5; // 初始位置在中间

        // 确保两张图片都已加载
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

        // 初始滑块位置
        updateSliderPosition();
    }

    damageLevelSelector.addEventListener('change', function() {
        const selectedLevel = this.value;
        damageDescription.textContent = damageLevelDescriptions[selectedLevel];
        updateDamageImage(selectedLevel);
    });

    function updateDamageImage(selectedLevel) {
        if (!damageData) return;

        const ctx = damageCanvas.getContext('2d');
        const imageData = ctx.getImageData(0, 0, damageCanvas.width, damageCanvas.height);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
            const pixelDamageLevel = damageData[i / 4];
            if (selectedLevel === 'all' || parseInt(selectedLevel) === pixelDamageLevel) {
                if (pixelDamageLevel > 0) {
                    const color = damageLevelColors[pixelDamageLevel];
                    data[i] = color[0];     // R
                    data[i + 1] = color[1]; // G
                    data[i + 2] = color[2]; // B
                    data[i + 3] = color[3]; // A
                } else {
                    data[i + 3] = 0; // 完全透明
                }
            } else {
                data[i + 3] = 0; // 完全透明
            }
        }

        ctx.putImageData(imageData, 0, 0);
    }

    // 在毁伤评估完成后调用这个函数
    function initializeDamageVisualization(damageImageData, originalImage) {
        damageData = new Uint8Array(damageImageData.length);
        for (let i = 0; i < damageImageData.length; i++) {
            damageData[i] = damageImageData.charCodeAt(i);
        }

        damageCanvas.width = originalImage.width;
        damageCanvas.height = originalImage.height;

        const ctx = damageCanvas.getContext('2d');
        ctx.drawImage(originalImage, 0, 0);

        damageImageContainer.innerHTML = '';
        damageImageContainer.appendChild(originalImage);
        damageImageContainer.appendChild(damageCanvas);
        damageCanvas.style.position = 'absolute';
        damageCanvas.style.top = '0';
        damageCanvas.style.left = '0';

        updateDamageImage('all');
    }

    startAssessmentButton.addEventListener('click', async function() {
        showMessage('正在进行毁伤评估...', 'info');

        const formData = new FormData();
        formData.append('original_image', dataURLtoBlob(originalImageSrc), 'original_image.png');
        formData.append('simulated_image', dataURLtoBlob(afterImage.src), 'simulated_image.png');

        try {
            const response = await fetch('http://localhost:5000/assess_damage', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.original_image && data.damage_data) {
                const originalImage = new Image();
                originalImage.onload = function() {
                    initializeDamageVisualization(atob(data.damage_data), originalImage);
                };
                originalImage.src = 'data:image/png;base64,' + data.original_image;

                damageStatistics.innerHTML = `
                    <p>无毁伤: ${data.damage_statistics['0'].toFixed(2)}%</p>
                    <p>1级毁伤: ${data.damage_statistics['1'].toFixed(2)}%</p>
                    <p>2级毁伤: ${data.damage_statistics['2'].toFixed(2)}%</p>
                    <p>3级毁伤: ${data.damage_statistics['3'].toFixed(2)}%</p>
                    <p>4级毁伤: ${data.damage_statistics['4'].toFixed(2)}%</p>
                `;
                showMessage('毁伤评估完成！', 'success');
                document.getElementById('assessment-result').style.display = 'block';
                document.getElementById('damage-assessment').style.display = 'block';
            } else {
                throw new Error('No damage data in response');
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('毁伤评估失败: ' + error.message, 'error');
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

    function showMessage(message, type) {
        const messageContainer = document.getElementById('message-container');
        messageContainer.textContent = message;
        messageContainer.className = `message ${type}`;
        messageContainer.style.display = 'block';
        setTimeout(() => {
            messageContainer.style.display = 'none';
        }, 6000);
    }
});