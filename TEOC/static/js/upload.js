Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#my-dropzone", {
    url: "upload_files",
    acceptedFiles: "application/pdf",
    autoProcessQueue: false,
    uploadMultiple: true,
    addRemoveLinks: true,
    parallelUploads:1/0,
    dictDefaultMessage:'Перетащите файлы или нажмите и загрузите их'
})


$('#submit-all').hide();

myDropzone.on("addedfile", function(file) {
    if(file.type.match('.pdf')){
        $('#submit-all').show();
    }
});

myDropzone.on("success", function () {
    setTimeout(function () {
        myDropzone.removeAllFiles(true);
    }, 2000);
});


$('#submit-all').click(function(){ 
    myDropzone.options['dictCancelUpload'] = "";
    myDropzone.processQueue();
    myDropzone.options['dictRemoveFile'] = "";
    $('#submit-all').hide();
});