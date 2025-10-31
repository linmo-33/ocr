// API基础URL
const API_BASE = window.location.origin;

// 当前选中的功能类型
let currentType = 'classification';

// 初始化
document.addEventListener('DOMContentLoaded', function () {
    initTabs();
    loadStats();
    setupEventListeners();
});

// 初始化标签页
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            const targetType = this.dataset.type;
            switchTab(targetType);
        });
    });
}

// 切换标签页
function switchTab(type) {
    currentType = type;

    // 更新标签样式
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`[data-type="${type}"]`).classList.add('active');

    // 更新内容显示
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${type}-content`).classList.add('active');
}

// 设置事件监听
function setupEventListeners() {
    // 文件上传预览
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', handleFileSelect);
    });

    // 表单提交
    document.getElementById('recognizeBtn').addEventListener('click', handleRecognize);
}

// 处理文件选择
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (event) {
        const base64 = event.target.result.split(',')[1];

        // 根据当前类型设置对应的输入框
        if (currentType === 'capcode' || currentType === 'slideComparison') {
            if (e.target.id === 'slidingImageFile') {
                document.getElementById('slidingImage').value = base64;
            } else if (e.target.id === 'backImageFile') {
                document.getElementById('backImage').value = base64;
            }
        } else {
            document.getElementById(`${currentType}Image`).value = base64;
        }

        // 显示预览
        showImagePreview(event.target.result, e.target.id);
    };
    reader.readAsDataURL(file);
}

// 显示图片预览
function showImagePreview(dataUrl, inputId) {
    const previewId = inputId.replace('File', 'Preview');
    let preview = document.getElementById(previewId);

    if (!preview) {
        preview = document.createElement('div');
        preview.id = previewId;
        preview.className = 'image-preview';
        document.getElementById(inputId).parentElement.appendChild(preview);
    }

    preview.innerHTML = `<img src="${dataUrl}" alt="预览">`;
}

// 处理识别请求
async function handleRecognize() {
    const btn = document.getElementById('recognizeBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="loading"></span> 识别中...';

    try {
        let endpoint, data;

        switch (currentType) {
            case 'classification':
                endpoint = '/classification';
                data = {
                    image: document.getElementById('classificationImage').value,
                    preprocess: document.getElementById('preprocessClassification').checked
                };
                break;

            case 'capcode':
                endpoint = '/capcode';
                data = {
                    slidingImage: document.getElementById('slidingImage').value,
                    backImage: document.getElementById('backImage').value,
                    simpleTarget: document.getElementById('simpleTarget').checked,
                    preprocess: document.getElementById('preprocessCapcode').checked
                };
                break;

            case 'slideComparison':
                endpoint = '/slideComparison';
                data = {
                    slidingImage: document.getElementById('slideImage').value,
                    backImage: document.getElementById('slideBackImage').value
                };
                break;

            case 'detection':
                endpoint = '/detection';
                data = {
                    image: document.getElementById('detectionImage').value
                };
                break;

            case 'calculate':
                endpoint = '/calculate';
                data = {
                    image: document.getElementById('calculateImage').value
                };
                break;

            case 'select':
                endpoint = '/select';
                data = {
                    image: document.getElementById('selectImage').value
                };
                break;

            case 'crop':
                endpoint = '/crop';
                data = {
                    image: document.getElementById('cropImage').value,
                    y_coordinate: parseInt(document.getElementById('yCoordinate').value)
                };
                break;

            case 'batch':
                endpoint = '/batch/classification';
                const imagesText = document.getElementById('batchImages').value;
                data = {
                    images: imagesText.split('\n').filter(img => img.trim()),
                    preprocess: document.getElementById('preprocessBatch').checked
                };
                break;
        }

        const response = await fetch(API_BASE + endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showResult(result, false);
        } else {
            showResult(result, true);
        }

        // 刷新统计
        loadStats();

    } catch (error) {
        showResult({ error: error.message }, true);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '开始识别';
    }
}

// 显示结果
function showResult(data, isError) {
    const resultBox = document.getElementById('resultBox');
    const resultContent = document.getElementById('resultContent');

    resultBox.style.display = 'block';
    resultBox.className = 'result-box ' + (isError ? 'error' : 'success');

    resultContent.textContent = JSON.stringify(data, null, 2);
}

// 加载统计信息
async function loadStats() {
    try {
        const response = await fetch(API_BASE + '/stats');
        const stats = await response.json();

        document.getElementById('totalRequests').textContent = stats.total_requests;
        document.getElementById('successRate').textContent = stats.success_rate;
        document.getElementById('avgTime').textContent = stats.average_processing_time;

    } catch (error) {
        console.error('加载统计失败:', error);
    }
}

// 复制结果到剪贴板
function copyResult() {
    const resultContent = document.getElementById('resultContent').textContent;
    navigator.clipboard.writeText(resultContent).then(() => {
        alert('已复制到剪贴板！');
    });
}

// 清空表单
function clearForm() {
    document.querySelectorAll('input[type="text"], textarea').forEach(input => {
        input.value = '';
    });
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });
    document.querySelectorAll('.image-preview').forEach(preview => {
        preview.remove();
    });
    document.getElementById('resultBox').style.display = 'none';
}
