AWS.config.update({
    accessKeyId: "AKIAR6NDCMA6WKKR6IUO",
    secretAccessKey: "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",
    region: 'us-east-1'
});
var s3 = new AWS.S3();

var vids=[];

var userName;

$(document).ready(function(){
	// console.log(getVideo());
	userName = window.localStorage.getItem("userName");
	if(userName != null){
		document.getElementById("lUser").innerHTML = userName.split(" ")[0];
	}

	var modal = document.getElementById("myModal");
	var span = document.getElementsByClassName("close")[0];


	$("#openUpload").click(function(){
		modal.style.display = "block";
		// upload();
	});

	span.onclick = function() {
  		modal.style.display = "none";
	}

	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
	  }
	}

	$("#uploadSubmit").click(function(){
		// alert("here");
		upload();
	});

	$("#logout").click(function(){
		logout();
	});

	$("#name").keyup(function(e){
		var inpt = $('#name').val().trim();
		if(inpt.length == 0){
			document.getElementById("uploadSubmit").disabled = true;
		}
		else{
			document.getElementById("uploadSubmit").disabled = false;
		}
	});

	load();

});

window.fbAsyncInit = function() {
    FB.init({
      appId      : '479583246665370',
      cookie     : true,                     // Enable cookies to allow the server to access the session.
      xfbml      : true,                     // Parse social plugins on this webpage.
      version    : 'v10.0'           // Use this Graph API version for this call.
    });

    FB.getLoginStatus(function(response) {   // Called after the JS SDK has been initialized.
      statusChangeCallback(response);        // Returns the login status.
    });
};

// TODO: Logout and redirect back to login 
function logout(){
	// alert("Here");
	console.log("logout");

	FB.logout(function(response) {
	   // user is now logged out
	   window.localStorage.removeItem("userID");	
	   window.localStorage.removeItem("userName");
	   window.location = "https://videonotes-site.s3.amazonaws.com/login.html";
	});	
}

function load(){

	var allKeys = [];

	var apigClient = apigClientFactory.newClient({
    accessKey: 'AKIASVTWRP3BCYAZ7X4T',
    secretKey: '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'
	});

	var params = {

	};

	var body = {
	  // This is where you define the body of the request,
	};

	var additionalParams = {

	};

	var allKeys = []
	var allTitle = []

	apigClient.rootGet(params, body, additionalParams)
	    .then(function(result){
	      // Add success callback code here.
	      
	      console.log(result);
	      result.data.forEach(function(item){
	      	allKeys.push(item);
	      });
	      updateThumbnails(allKeys)
	    }).catch( function(result){
	      console.log(result);
	    });
}

function updateThumbnails(result){

	console.log(result);
 //    console.log();

    var allItems = "";
	vids=[];
    var vid;

    result.forEach(function(item){
    	id = item["video_id"]
    	// console.log(item["video_id"])
    	// console.log(id);
    	var vidTag = '<div class="w3-card-4 align-item-center bgc" onclick="openVideo(\''+id+'\')" style="width:350px;height:310px"><video width="350px" preload="metadata" id="'+item['video_id']+'"><source src="'+item['video_url']+'#t=.1" type="video/mp4"></video><hr />';
    	// var label = '<br><b>'+item['video_title']+'</b>'
    	var label = '<div class="w3-container w3-center vidTitle">'+item['video_title']+'</div></div>'
    	var gridItem = '<div class="grid-item">'+vidTag+label+'</div>';

    	allItems = allItems + gridItem;
    	// console.log(item)
    	var vid = {
    		'video_id': id,
    		'video_url': item['video_url'],
    		'video_title': item['video_title']
    	};
    	vids.push(vid);

    });
    var grid = document.getElementById("thumbnails");
    grid.innerHTML = allItems

}

//TODO: redirect to index page and display video
function openVideo(id){
	window.location = "https://videonotes-site.s3.amazonaws.com/index.html?v="+id;
}

function upload(){
	var file = document.getElementById("upload").files[0]
	var name = $('#name').val().trim();
	if(name.length == 0){
		name = file.name;
	}

	console.log(name)
	// const fileContent = fs.readFileSync(file);
	const params = {
		Bucket: "project-cu-videos",
		Key: file.name,
		Body: file,
		Metadata:{
			'customlabels': name
		}
	}

	document.getElementById("myModal").style.display = "none";
	document.getElementById("upload").value = "";
	$('#name').val("");
	document.getElementById("uploadSubmit").disabled = true;
	console.log("upload successfull");
	
	s3.upload(params, function(err, data) {
		if(err){
			throw err;
		}
	})
}