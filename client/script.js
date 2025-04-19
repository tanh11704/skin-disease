// Xử lý kéo thả ảnh
const dropArea = document.getElementById('dropArea');

dropArea.addEventListener('click', () => {
    document.getElementById('skinImage').click();
});

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.style.borderColor = '#3498db';
    dropArea.style.backgroundColor = 'rgba(52, 152, 219, 0.1)';
});

dropArea.addEventListener('dragleave', () => {
    dropArea.style.borderColor = '#ccc';
    dropArea.style.backgroundColor = 'transparent';
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.style.borderColor = '#ccc';
    dropArea.style.backgroundColor = 'transparent';
    
    if (e.dataTransfer.files.length) {
        document.getElementById('skinImage').files = e.dataTransfer.files;
        previewImage(e.dataTransfer.files[0]);
    }
});

// Xem trước ảnh khi upload
document.getElementById('skinImage').addEventListener('change', function(e) {
    if (e.target.files.length) {
        previewImage(e.target.files[0]);
    }
});

function previewImage(file) {
    const preview = document.getElementById('imagePreview');
    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';
}

// Hàm chẩn đoán (giả lập)
function diagnose() {
    // Kiểm tra xem có ảnh được chọn không
    const fileInput = document.getElementById('skinImage');
    if (fileInput.files.length === 0) {
        alert('Vui lòng chọn ảnh để chẩn đoán!');
        return;
    }
    
    // Hiển thị loader
    document.getElementById('loader').style.display = 'block';
    document.getElementById('resultContainer').style.display = 'none';
    
    // Giả lập thời gian xử lý AI
    setTimeout(() => {
        // Ẩn loader và hiển thị kết quả
        document.getElementById('loader').style.display = 'none';
        document.getElementById('resultContainer').style.display = 'block';
        
        // Giả lập kết quả
        document.getElementById('diseaseName').textContent = 'Vảy nến (Psoriasis)';
        document.getElementById('confidenceLevel').textContent = 'Độ chính xác: 92%';
        document.getElementById('resultImage').src = '/api/placeholder/400/320';
        document.getElementById('diseaseDescription').innerHTML = `
            <p>Vảy nến là một bệnh lý tự miễn mãn tính với đặc trưng là các mảng da đỏ, dày, bong vảy màu bạc. Bệnh thường tái phát và có thể ảnh hưởng đến chất lượng cuộc sống.</p>
            <p><strong>Nguyên nhân:</strong> Sự tăng sinh bất thường của tế bào da, thường do yếu tố di truyền và kích hoạt bởi môi trường.</p>
        `;
        
        // Thêm tin nhắn vào chat bot
        addChatMessage('Bot', 'Tôi đã phát hiện bạn có thể mắc bệnh vảy nến. Bạn có muốn biết cách điều trị hoặc có câu hỏi nào không?');
    }, 2000);
}

// Hàm chat
function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (message) {
        addChatMessage('Bạn', message);
        input.value = '';
        
        // Giả lập phản hồi từ bot sau một khoảng thời gian ngắn
        setTimeout(() => {
            let botResponse;
            
            // Logic phản hồi đơn giản dựa trên từ khóa
            if (message.toLowerCase().includes('điều trị') || message.toLowerCase().includes('chữa')) {
                botResponse = 'Đối với vảy nến, các phương pháp điều trị phổ biến bao gồm:<br>1. Thuốc bôi ngoài da chứa corticosteroid<br>2. Liệu pháp ánh sáng (phototherapy)<br>3. Thuốc uống đặc trị như methotrexate, cyclosporine<br>4. Thuốc sinh học cho các trường hợp nặng<br><br>Tôi khuyên bạn nên gặp bác sĩ da liễu để được tư vấn phương pháp điều trị phù hợp nhất.';
            } else if (message.toLowerCase().includes('nguyên nhân') || message.toLowerCase().includes('tại sao')) {
                botResponse = 'Vảy nến có nhiều nguyên nhân, bao gồm:<br>- Yếu tố di truyền (có tính gia đình)<br>- Rối loạn hệ miễn dịch<br>- Các yếu tố kích hoạt như stress, nhiễm trùng, thời tiết lạnh, thuốc, chấn thương da<br>- Lối sống không lành mạnh (hút thuốc, uống rượu)';
            } else if (message.toLowerCase().includes('phòng ngừa') || message.toLowerCase().includes('tránh')) {
                botResponse = 'Để phòng ngừa và giảm tần suất bùng phát vảy nến, bạn nên:<br>1. Giữ da ẩm thường xuyên<br>2. Tránh các chất kích thích da<br>3. Giảm stress<br>4. Tránh tổn thương da<br>5. Duy trì lối sống lành mạnh, hạn chế rượu bia và thuốc lá<br>6. Tiếp xúc với ánh nắng vừa phải (dưới sự hướng dẫn y tế)';
            } else {
                botResponse = 'Tôi hiểu mối quan tâm của bạn. Để tư vấn chính xác hơn về tình trạng vảy nến, tôi khuyên bạn nên thăm khám bác sĩ da liễu. Bạn còn câu hỏi nào khác về bệnh da liễu không?';
            }
            
            addChatMessage('Bot', botResponse);
        }, 800);
    }
}

function addChatMessage(sender, message) {
    const chat = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = sender === 'Bạn' ? 'message user-message' : 'message bot-message';
    msgDiv.innerHTML = message;
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
}