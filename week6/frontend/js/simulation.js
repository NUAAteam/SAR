document.addEventListener('DOMContentLoaded', function() {
    const uploadButton = document.getElementById('upload-button');
    const fileInput = document.getElementById('image-file');
    const uploadStatus = document.getElementById('upload-status');
    const uploadedImages = document.getElementById('uploaded-images');
    const imageSelect = document.getElementById('image-select');
    const damageSimulationButton = document.getElementById('damage-simulation');
    const sarSimulationButton = document.getElementById('sar-simulation');

    // 检查是否有之前上传的图片
    const savedImages = JSON.parse(localStorage.getItem('uploadedImages')) || [];

    // 如果有保存的图片,则显示它们
    savedImages.forEach(imageName => {
        const option = document.createElement('option');
        option.value = imageName;
        option.textContent = imageName;
        imageSelect.appendChild(option);

        const img = document.createElement('img');
        img.src = localStorage.getItem(imageName);
        img.alt = imageName;
        uploadedImages.appendChild(img);
    });

    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        const files = this.files;
        if (files.length > 0) {
            uploadStatus.textContent = '正在处理...';
            handleFiles(files);
        }
    });

    function handleFiles(files) {
        for (let file of files) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.alt = file.name;
                uploadedImages.appendChild(img);

                const option = document.createElement('option');
                option.value = file.name;  // 存储文件名
                option.textContent = file.name;
                imageSelect.appendChild(option);

                // 将图片数据存储在 localStorage 中
                localStorage.setItem(file.name, e.target.result);

                // 更新保存的图片列表
                const savedImages = JSON.parse(localStorage.getItem('uploadedImages')) || [];
                if (!savedImages.includes(file.name)) {
                    savedImages.push(file.name);
                    localStorage.setItem('uploadedImages', JSON.stringify(savedImages));
                }
            };
            reader.readAsDataURL(file);
        }
        uploadStatus.textContent = '处理完成!';
    }

    damageSimulationButton.addEventListener('click', function() {
        const selectedImageName = imageSelect.value;
        if (selectedImageName) {
            console.log('Selected image name:', selectedImageName);
            // 使用 URL 参数传递选中的图片名称
            window.location.href = `damage_simulation.html?image=${encodeURIComponent(selectedImageName)}`;
        } else {
            alert('请先选择一张图片');
        }
    });

    sarSimulationButton.addEventListener('click', function() {
        const selectedImageName = imageSelect.value;
        if (selectedImageName) {
            window.location.href = `sar_simulation.html?image=${encodeURIComponent(selectedImageName)}`;
        } else {
            alert('请先选择一张图片');
        }
    });
});