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
    const damageCanvas = document.createElement('canvas');
    const damageImageContainer = document.getElementById('damage-image-container');

    let selectedX = null;
    let selectedY = null;
    let originalImageWidth = null;
    let originalImageHeight = null;
    let originalImageSrc = null;
    let simulatedImage = null;
    let damageData = null; // 用于存储毁伤数据

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

    startAssessmentButton.addEventListener('click', assessDamage);

    function assessDamage() {
        showMessage('正在进行毁伤评估...', 'info');

        fetch('http://localhost:5000/assess_damage', {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.blob();
        })
        .then(blob => {
            const imageUrl = URL.createObjectURL(blob);
            damageImage.src = imageUrl;
            damageImage.onload = function() {
                damageImage.style.display = 'block';
                document.getElementById('assessment-result').style.display = 'block';
            };
            return fetch('http://localhost:5000/get_damage_statistics');
        })
        .then(response => response.json())
        .then(data => {
            updateDamageStatistics(data.damage_statistics);
            showMessage('毁伤评估完成！', 'success');
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('毁伤评估失败: ' + error.message, 'error');
        });
    }

    function updateDamageStatistics(statistics) {
        let html = '<ul class="damage-stats-list">';
        const damageLabels = {
            1: '轻微毁伤',
            2: '中等毁伤',
            3: '严重毁伤',
            4: '完全毁伤'
        };
        for (let level in statistics) {
            if (level == 0) continue; // 跳过无毁伤
            const percentage = statistics[level].toFixed(2);
            let barWidth = Math.min(percentage * 10, 100);
            html += `
                <li class="damage-stat-item level-${level}">
                    <span class="damage-level">${damageLabels[level]}</span>
                    <div class="damage-bar-container">
                        <div class="damage-bar" style="width: ${barWidth}%"></div>
                        <span class="damage-percentage">${percentage}%</span>
                    </div>
                </li>`;
        }
        html += '</ul>';
        damageStatistics.innerHTML = html;
    }

    function showMessage(message, type) {
        const messageContainer = document.getElementById('message-container');
        messageContainer.textContent = message;
        messageContainer.className = `message ${type}`;
        messageContainer.style.display = 'block';
        setTimeout(() => {
            messageContainer.style.display = 'none';
        }, 5000);
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

    // 添加颜色图例
    function addColorLegend() {
        let legendHtml = `
            <div class="color-legend">
                <div><span style="background-color: yellow;"></span> 1级毁伤</div>
                <div><span style="background-color: green;"></span> 2级毁伤</div>
                <div><span style="background-color: red;"></span> 3级毁伤</div>
                <div><span style="background-color: blue;"></span> 4级毁伤</div>
            </div>
        `;
        $('#colorLegend').html(legendHtml);
    }

    // 在页面加载时调用
    $(document).ready(function() {
        addColorLegend();
    });
});