let diseaseMapping = {
    "Acne": "Mụn trứng cá",
    "Actinic_Keratosis": "Dày sừng quang hóa",
    "Benign_tumors": "U lành tính",
    "Bullous": "Bệnh bóng nước",
    "DrugEruption": "Phản ứng do thuốc",
    "Eczema": "Chàm",
    "Infestations_Bites": "Ký sinh trùng/Côn trùng cắn",
    "Lichen": "Lichen",
    "Moles": "Nốt ruồi",
    "Psoriasis": "Vảy nến",
    "Rosacea": "Chứng đỏ mặt",
    "Seborrh_Keratoses": "Dày sừng bã nhờn",
    "SkinCancer": "Ung thư da",
    "Sun_Sunlight_Damage": "Tổn thương do ánh nắng",
    "Tinea": "Bệnh nấm da",
    "Unknown_Normal": "Da bình thường/Chưa xác định",
    "Vascular_Tumors": "U mạch máu",
    "Vasculitis": "Viêm mạch máu",
    "Vitiligo": "Bạch biến",
    "Warts": "Mụn cóc",
    "Urticaria": "Mề đay",
    "Varicella": "Thủy đậu",
    "Herpes_Zoster": "Thủy đậu lở"
};

let diseaseDescriptionMapping = {
    "Acne": "Là một bệnh lý da liễu phổ biến xảy ra khi lỗ chân lông bị tắc bởi dầu(bã nhờn), tế bào da chết hoặc vi khuẩn, và xuất hiện nhiều nhất ở độ tuổi dậy thì – khoảng thời gian có sự thay đổi về hormone trong cơ thể.",
    "Actinic_Keratosis": "Tình trạng một vùng da thô ráp, có vảy, do tiếp xúc lâu dài với ánh sáng mặt trời, đặc biệt là trên mặt, tay, cánh tay và cổ. Căn bệnh này thường gặp ở những người da trắng, mắt xanh. Đây là tình trạng tiền ung thư da có thể dẫn đến ung thư biểu mô tế bào vảy.",
    "Benign_tumors": "Là sự phát triển bất thường của tế bào nhưng không lan rộng và di căn sang các cơ quan khác và không gây ung thư. Các khối u lành tính có thể hình thành ở bất cứ đâu.  Bất cứ ai cũng có thể có một khối u lành tính, bao gồm cả trẻ em, mặc dù người lớn có nhiều khả năng bị tình trạng này hơn.",
    "Bullous": "Là nhóm các bệnh da hiếm đặc trưng bởi sự hình thành bóng nước hoặc phỏng nước lớn trên da và niêm mạc, có thể do tự miễn hoặc các yếu tố khác. Bệnh hay gặp ở người lớn tuổi, từ 50-60 tuổi trở lên, đặc biệt là trên 70 tuổi, có thể gặp ở người trẻ nhưng rất hiếm ở trẻ em.",
    "DrugEruption": "Drug Eruption là phản ứng dị ứng da đặc biệt do thuốc gây ra, là những biểu hiện rất thường gặp có thể từ nhẹ như nổi mẩn đến nặng như hội chứng Stevens-Johnson hoặc sốc phản vệ.",
    "Eczema": "Eczema là một tình trạng viêm da mãn tính với cơ chế bệnh sinh phức tạp liên quan đến tính nhạy cảm di truyền, rối loạn chức năng miễn dịch và biểu bì, và các yếu tố môi trường. Không lây, thường gây ngứa, đỏ, khô và tổn thương da, thường liên quan đến cơ địa dị ứng và miễn dịch.",
    "Infestations_Bites": "Là nhóm bệnh do nhiễm ký sinh trùng ngoài da hoặc bị côn trùng đốt, gây tổn thương da, ngứa, dị ứng hoặc lây truyền bệnh. Thông qua các đường lây nhiễm như lây qua đất, qua da, đường tiêu hóa, từ động vật sang người…. Mức độ bệnh tiến triển chậm nhưng nếu không phát hiện và điều trị kịp thời sẽ gây ảnh hưởng xấu đến sức khỏe người bệnh.",
    "Lichen": "Lichen là một bệnh viêm da mạn tính, không lây, có thể ảnh hưởng đến da, niêm mạc miệng, vùng sinh dục và móng tay, gây ngứa và tổn thương đặc trưng. Là một bệnh ngoài da tuy không nguy hiểm nhưng lại kéo dài và dễ tái phát.",
    "Moles": "Là sự phát triển lành tính của tế bào sắc tố dưới da, thường xuất hiện dưới dạng các đốm nhỏ có màu nâu, đen hoặc hồng. Có thể bắt gặp nốt ruồi ở bất cứ đâu trên cơ thể như lòng bàn tay, lòng bàn chân, da đầu, móng tay, mắt hoặc ở cả bộ phận sinh dục. Nốt ruồi thường có sự thay đổi chậm về hình dáng và số lượng, có thể đổi màu nhẹ hoặc nhô cao lên hoặc có khi mọc thêm lông. Nốt ruồi cũng có thể mờ dần và biến mất sau đó.",
    "Psoriasis": "Psoriasis là bệnh viêm da mạn tính tự miễn, khiến tế bào da phát triển nhanh bất thường, gây bong tróc và đóng vảy. Bệnh có thể xảy ra ở mọi lứa tuổi, trong đó có cả trẻ em. Bệnh vảy nến là một bệnh mãn tính, không thể chữa khỏi hoàn toàn,nhưng có thể kiểm soát để bệnh ổn định và không bùng phát.",
    "Rosacea": "Là bệnh viêm da mãn tính không lây, thường ảnh hưởng vùng mặt với biểu hiện đỏ da, giãn mạch và có thể nổi mụn. Là một hiện tượng khá phổ biến, có thể xuất hiện ở bất kỳ ai, nhưng thường gặp nhất ở những phụ nữ trung niên với làn da sáng màu.",
    "Seborrh_Keratoses": "Là một dạng tổn thương da lành tính thường gặp ở người lớn tuổi, có dạng mảng gồ sần sùi như sáp dính trên da.",
    "SkinCancer": "Là bệnh lý ác tích do tình trạng các tế bào da phát triển bất thường không kiểm soát, có thể gây xâm lấn và di căn nếu không phát hiện kịp thời. Ung thư da thường xuất hiện trên các vùng da tiếp xúc trực tiếp với ánh nắng mặt trời, nhưng cũng có thể gặp phải ở các vùng da khác.",
    "Sun_Sunlight_Damage": "Là tình trạng tổn thương trên da do tiếp xúc trực tiếp một lượng quá nhiều ánh nắng mặt trời và tia cực tím vượt quá hàm lượng sắc tố melanin để bảo vệ da của cơ thể. Là hậu quả của việc tiếp xúc quá mức với tia UV, có thể gây cháy nắng, lão hóa sớm và ung thư da.",
    "Tinea": "Tinea là nhóm bệnh nhiễm nấm ngoài da, ảnh hưởng đến da, tóc hoặc móng, do vi nấm dermatophyte gây ra. Nấm da Tinea là tên gọi của bệnh lý về da do nhiễm nấm khi biểu hiện lâm sàng bị thay đổi do điều trị không thích hợp, thường là bôi kem steroid.",
    "Unknown_Normal": "Là tình trạng bình thường, không có triệu chứng hoặc không có vấn đề sức khỏe rõ ràng.",
    "Vascular_Tumors": "Là các khối u lành tính hoặc ác tính có nguồn gốc từ các mạch máu, thường gặp nhất là u máu (hemangioma) ở trẻ sơ sinh. Thường là những tổn thương không đau và khối u máu có màu đỏ hoặc xanh. Thông thường, khối u này bằng phẳng hoặc hơi gồ ghề trên da, vì vậy rất dễ xảy ra tình trạng chảy máu, viêm loét nếu có va đập trong quá trình sinh hoạt hàng ngày.",
    "Vasculitis": "Là tình trạng viêm của các mạch máu, làm thay đổi cấu trúc thành mạch, gây hẹp, tắc nghẽn hoặc vỡ mạch, ảnh hưởng đến lưu lượng máu đến các cơ quan.",
    "Vitiligo": "Là một rối loạn sắc tố da mạn tính, trong đó các tế bào tạo sắc tố (melanocyte) bị phá hủy, dẫn đến các mảng da mất màu. Bệnh bạch biến có thể gặp mọi lứa tuổi và mọi giới. Lứa tuổi thường gặp nhất là từ 10-30, hơn 50% xảy ra trước 20 tuổi và có thể gặp bệnh bạch biến ở trẻ em.",
    "Warts": "Là các nốt u nhỏ, sần sùi trên da, thường do nhiễm virus HPV (Human Papillomavirus). Mụn cóc có thể xuất hiện ở bất kỳ vị trí nào trên cơ thể. Mụn cóc là một trong những bệnh da liễu lành tính phổ biến hiện nay. Mặc dù ít ảnh hưởng đến sức khỏe nhưng lại có khả năng “nhảy” sang các vùng da hoặc người khác khi tiếp xúc, gây mất thẩm mỹ.",
    "Urticaria": "Là tình trạng mao mạch da phản ứng với các tác nhân khác nhau, phản ứng da thường gặp,một dạng phát ban ngứa trên da biểu hiện bằng các mảng hoặc sẩn phù nông, gây ngứa, do phản ứng quá mẫn hoặc kích thích hệ miễn dịch.",
    "Varicella": "Thủy đậu là bệnh nhiễm virus do varicella-zoster gây ra, đặc trưng bởi phát ban dạng mụn nước ngứa, thường gặp ở trẻ em nhưng có thể mắc ở người lớn, lây chủ yếu qua đường hô hấp (hoặc không khí). Không có triệu chứng nặng nề ngoài những mụn nước nhưng rất dễ gây nhiễm trùng da nơi mọc mụn nước, có thể dẫn đến nhiễm trùng huyết, viêm não.... Đây là bệnh có khả năng lây lan nhanh chóng, có thể xảy ra ở cả trẻ em (phổ biến hơn) và người lớn. ",
}

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

async function diagnose(event) {
    if (event) {
        event.preventDefault();
    }
    
    const fileInput = document.getElementById('skinImage');
    if (fileInput.files.length === 0) {
        alert('Vui lòng chọn ảnh để chẩn đoán!');
        return;
    }
    
    document.getElementById('loader').style.display = 'block';
    document.getElementById('resultContainer').style.display = 'none';
    
    try {
        const formData = new FormData();
        formData.append('image', fileInput.files[0]);

        const response = await fetch('http://localhost:8000/api/upload/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Lỗi API: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();

        document.getElementById('loader').style.display = 'none';
        document.getElementById('resultContainer').style.display = 'block';

        document.getElementById('diseaseName').textContent = diseaseMapping[data.prediction];
        document.getElementById('confidenceLevel').textContent = `Độ chính xác: ${(data.confidence*100).toFixed(2)}%`;
        document.getElementById('resultImage').src = data.image_url;

        document.getElementById('skinImage').value = '';
        document.getElementById('imagePreview').style.display = 'none';

        document.getElementById('diseaseDescription').innerHTML = diseaseDescriptionMapping[data.prediction] || 'Không có thông tin mô tả cho bệnh này.';
    } catch (error) {
        console.error('Lỗi khi gọi API:', error);
        document.getElementById('loader').style.display = 'none';
        document.getElementById('resultContainer').style.display = 'block';

        document.getElementById('diseaseName').textContent = 'Lỗi';
        document.getElementById('confidenceLevel').textContent = '';
        addChatMessage('Bot', 'Đã xảy ra lỗi khi chẩn đoán. Bạn có muốn thử lại không?');
    }
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