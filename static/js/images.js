const imageInput = document.getElementById('image-input');
const imagePreview = document.getElementById('image-preview');

    imageInput.addEventListener('change', function(event) {
        const files = event.target.files;

        // Очистка контейнера предварительного просмотра
        imagePreview.innerHTML = '';

        if (files.length > 10) {
            alert('Вы можете загрузить только 10 изображений.');
            imageInput.value = ''; // Сброс
            return;
        }

        for (let i = 0; i < files.length; i++) {
            if (i >= 10) break; // Ограничение в 10 изображений

            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('preview-image');
                imagePreview.appendChild(img);
            };
            reader.readAsDataURL(files[i]);
        }
    });