function handleFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();

    var files = evt.dataTransfer.files; // FileList object.

    var file = files[0];
    var reader = new FileReader();
    reader.onload = (function(theFile) {
        return function(e) {
            $.ajax({
                url: '/',
                type: 'POST',
                data: e.target.result,
                processData: false,
                contentType: 'application/pdf'
            }).done(function(response) {
                alert(response);
            });
        };
    })(file);

    reader.readAsDataURL(file);
}

function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy'; 
}

var dropZone = document.getElementById('drop_zone');
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileSelect, false);
