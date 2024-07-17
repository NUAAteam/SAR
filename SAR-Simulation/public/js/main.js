function uploadFiles() {
  const input = document.getElementById('fileInput');
  const files = input.files;
  const formData = new FormData();

  for (let i = 0; i < files.length; i++) {
    formData.append('images', files[i]);
  }

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => response.text())
  .then(data => {
    alert(data);
    populateFileSelect(files);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function populateFileSelect(files) {
  const fileSelect = document.getElementById('fileSelect');
  fileSelect.innerHTML = '<option value="">选择图片</option>';

  for (let i = 0; i < files.length; i++) {
    const option = document.createElement('option');
    option.value = files[i].name;
    option.text = files[i].name;
    fileSelect.appendChild(option);
  }
}

function simulate() {
  const fileSelect = document.getElementById('fileSelect');
  const actionSelect = document.getElementById('actionSelect');

  const fileName = fileSelect.value;
  const action = actionSelect.value;

  if (!fileName || !action) {
    alert('请选择图片和操作');
    return;
  }

  fetch('/simulate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ fileName, action })
  })
  .then(response => response.text())
  .then(data => {
    const resultImage = document.getElementById('resultImage');
    resultImage.src = data;
    resultImage.style.display = 'block';
  })
  .catch(error => {
    console.error('Error:', error);
  });
}
