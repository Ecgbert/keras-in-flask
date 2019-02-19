function getFile() {
	document.getElementById("upload_btn").click();
}

$('#upload_btn').change(function() {
	$('#Upload_Name').text(this.files[0].name);
});
$("#upload_btn").change(function() {
	readFile(this);
});

function readFile(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();
		reader.onload = function(e) {
			$('#ImagePreview').attr("src", e.target.result);
		}
		reader.readAsDataURL(input.files[0]);
	}
}
// ajax 上傳
$('#upload_btn').change(function() {
    $('.loader').show();
    $("#list_results").html('');
	var formDataRaw = $("#UploadForm")[0];
	//        console.log(formDataRaw)
	var form_data = new FormData(formDataRaw);
	$.ajax({
		type: 'POST',
		url: '/upload',
		data: form_data,
		contentType: false,
		cache: false,
		processData: false,
		async: true,
		success: function(data) {
			console.log('Success!');
			$('.loader').hide();
			$('#results-text').text("辨識結果:");
			$.each(data.predictions, function(i, item) {
			    label = item["label"];
			    prob = item["probability"].toFixed(4);
			    percent = prob * 100;
			    $('#list_results').append('<li class="list-group-item d-flex justify-content-between align-items-center">' + label +
			    '<span class="badge badge-primary badge-pill">' + prob + '</span></li>');
			});
		},
	});
});

$('#camVisualize').click(function() {
    var formDataRaw = $("#UploadForm")[0];
    var form_data = new FormData(formDataRaw);
    $.ajax({
        type: 'POST',
        url: '/grad-cam',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(json_data){
            console.log(json_data);
            $('#gradcam_result').text("Visualize:");
            $('#GradCamImage').attr("src", "data:image/jpg;base64," + json_data);
        }
    })
})