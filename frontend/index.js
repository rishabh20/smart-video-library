AWS.config.update({
    accessKeyId: "AKIAR6NDCMA6WKKR6IUO",
    secretAccessKey: "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",
    region: 'us-east-1'
});
var s3 = new AWS.S3;

var currentVid = "";
var video_id;	
var user_id;
var userName;


$(document).ready(function(){

	// document.getElementById("lUser").innerHTML = window.localstorage.getItem("userName");

	userName = window.localStorage.getItem("userName");
	document.getElementById("lUser").innerHTML = userName.split(" ")[0];

	video_id = window.location.search;	
	video_id = video_id.substring(3, video_id.length);	
	user_id = window.localStorage.getItem("userID");

	// console.log(getVideo());
	var modal = document.getElementById("myModal");
	var span = document.getElementsByClassName("close")[0];

	var modalCloud = document.getElementById("cloud");
	var spanCloud = document.getElementsByClassName("close")[1];

	$("#openUpload").click(function(){
		modal.style.display = "block";
	});

	$("#openWordCloud").click(function(){
		modalCloud.style.display = "block";
	});

	$("#btn1").click(function(){
		deleteNote('btn1');
	})
  		
	span.onclick = function() {
		modal.style.display = "none";
	}
	spanCloud.onclick = function() {
		modalCloud.style.display = "none";
	}

	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
	  }
	  if (event.target == modalCloud) {
	    modalCloud.style.display = "none";
	  } 
	}

	$("#uploadSubmit").click(function(){
		// alert("here");
		upload();
	});

	$("#logout").click(function(k){
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

	$("#notesText").keyup(function(e){
		var inpt = $('#notesText').val().trim();
		if(inpt.length == 0){
			document.getElementById("save").disabled = true;
			$("#save").removeClass("s_hover");
		}
		else{
			document.getElementById("save").disabled = false;
			$("#save").addClass("s_hover");
		}
	});

  		$("#search").keyup(function(e){
  			var inpt = $('#search').val().trim();
			if(e.keyCode == 13 && inpt.length>0){
				// alert("search");
				$('#search').val("");
				search(inpt);
			}
		});

		$("#save").click(function(){
			document.getElementById("save").disabled = false;
			$("#save").removeClass("s_hover");
			save()
		});

		$("#uploadSubmit").click(function(){
			// alert("here");
			upload();
		});

		load();



});

//TODO: save notes
function save(){
	time = (document.getElementById("video").currentTime);
	let t = parseInt(time);
    newTime = (parseInt(t/60) + ':' + (t%60 < 10 ? '0' + t%60 : t%60));
	text = $('#notesText').val();
	console.log(newTime, text);
		
	var apigClient = apigClientFactory.newClient({	
	    accessKey: 'AKIASVTWRP3BCYAZ7X4T',	
	    secretKey: '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'	
	});	
	var request_body = {	
	    "userID" : user_id,	
	    "videoID" : video_id,	
	    "entry" : text,	
	    "timestamp" : newTime	
	}	
	apigClient.notesPost({}, request_body, {})	
		.then(function(result){	
		      console.log(result);	
		      var note_id = result.data['body']['note_id']	
		      console.log(note_id)	
		      $('#notesText').val("");		
		      updateNote(time, newTime, text, note_id);	

		}).catch( function(result){	
		      console.log(result);	
		});
}

function setCurrentTime(time){
	document.getElementById("video").currentTime = time;
}

function updateNote(time, newTime, text, note_id){	
	timeLink = "<a href='' onclick='setCurrentTime("+time+"); return false;'>"+newTime+"</a>"	
	tags = "<td>"+text+"</td><td style='text-align: center;'>"+timeLink+"</td><td style='text-align: center;'>"	
	tags = tags + "<button onclick='deleteNote("+note_id+")' id='"+note_id+"'>x</button></td>"	
	document.getElementById("displayNotes").insertRow(-1).innerHTML = tags	
}

function updateSearch(time, text){
	let t = parseInt(time);
	var newTime = (parseInt(t/60) + ':' + (t%60 < 10 ? '0' + t%60 : t%60));
	
	timeLink = "<a href='' onclick='setCurrentTime("+time+"); return false;'>"+newTime+"</a>"
	tags = "<td>"+text+"</td><td style='text-align: center;'>"+timeLink+"</td>"
	document.getElementById("displaySearch").insertRow(-1).innerHTML = tags
}

function search(inpt){
	// var userID = window.localstorage.getItem("userID");
	// console.log("userID");
	// var query = window.location.search
	// var vid = query.substring(3,query.length);

	// var vid = "d0de75dc34509d3a28e32963d5f025f6-2";

	var apigClient = apigClientFactory.newClient({
    	accessKey: 'AKIASVTWRP3BCYAZ7X4T',
    	secretKey: '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'
	});

	var params = {
		'v': video_id,
		'q': inpt
	};

	console.log(params);

	var body = {
	  // This is where you define the body of the request,
	};

	var additionalParams = {

	};

	apigClient.searchGet(params, body, additionalParams)
	    .then(function(result){	      
	      console.log(result);
	      // alert("done");
	      displaySearch(result.data['body']);
	      // result.data.forEach(function(item){
	      // 	allKeys.push(item);
	      // });
	      // updateThumbnails(allKeys)
	    }).catch( function(result){
	      console.log(result);
	});
}

function displaySearch(result){
	console.log(result);
	var records = result['records'];
	if(records.length > 0){
		$("#displaySearch").removeClass("hide");
		$("#noSearch").addClass("hide");
		clearSearch();
		records.forEach(function(item){
			updateSearch(item['timestamp'],item['sentence']);
		});
	}
	else{
		$("#displaySearch").addClass("hide");
		$("#noSearch").removeClass("hide");
	}	
}

function displayLoadNote(result){
	// console.log(result);
	var notes = result['notes'];
	if(notes.length > 0){
		// $("#displaySearch").removeClass("hide");
		// $("#noSearch").addClass("hide");
		notes.forEach(function(item){
			var newTime = item['timestamp'];
			var text = item['entry'];
			var note_id = item['note_id'];

			var mins= newTime.split(":")[0];
			var sec = newTime.split(":")[1];

			time = parseInt(mins)*60 + parseInt(sec)
			time = time.toString();
			timeLink = "<a href='' onclick='setCurrentTime("+time+"); return false;'>"+newTime+"</a>"	
			tags = "<td>"+text+"</td><td style='text-align: center;'>"+timeLink+"</td><td style='text-align: center;'>"	
			tags = tags + "<button onclick='deleteNote("+note_id+")' id='"+note_id+"'>x</button></td>"	
			document.getElementById("displayNotes").insertRow(-1).innerHTML = tags	
		});
	}
	else{
		// $("#displaySearch").addClass("hide");
		// $("#noSearch").removeClass("hide");
	}	
}


//TODO: play correct video
function load(){

	var video = document.getElementById('video');
	var source = document.createElement('source');

	var video_url;
	var video_title;
	var wordcloud_url;

	var apigClient = apigClientFactory.newClient({
	    accessKey: 'AKIASVTWRP3BCYAZ7X4T',
	    secretKey: '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'
	});

	params = {
		'v': video_id 
	}

	apigClient.watchGet(params, {}, {})
	    .then(function(result){
	        console.log(result);
	        var dict = result.data;
	        console.log(dict);
	        video_url = dict.video_url;
	        video_title = dict['video_title'];
	        wordcloud_url = dict["wordcloud_url"];

			console.log(video_url);
			console.log(video_title);
			console.log(wordcloud_url);

			source.setAttribute('src', video_url);
			document.getElementById('videoLbl').innerHTML = video_title;
			video.appendChild(source);

			// wordcloud_url = "https://project-cu-wordcloud.s3.amazonaws.com/transcript_2021-04-26T20_32_14.805Z.png";
			document.getElementById('cloudImg').innerHTML = "<img src='"+wordcloud_url+"'>";

			loadNotes();

	    }).catch( function(result){
	    	  console.log("Error occurred.");
	      	  console.log(result);
	});
}


		
function deleteNote(id){	
	$("#"+id+"").closest("tr").remove();	
	var apigClient = apigClientFactory.newClient({		
	    accessKey: 'AKIASVTWRP3BCYAZ7X4T',		
	    secretKey: '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'		
	});	
		
	var params = {	
		'noteID': id	
	};	
	apigClient.notesDelete(params,{},{});	
}

function loadNotes(){	
	var apigClient = apigClientFactory.newClient({		
	    accessKey: 'AKIASVTWRP3BCYAZ7X4T',		
	    secretKey: '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'		
	});	
	var params = {	
		'userID': user_id,	
		'videoID': video_id	
	}	
	apigClient.notesGet(params, {}, {})	
	    .then(function(result){	
	        var notes_list = result.data['body'];	
	        console.log(notes_list);
	        displayLoadNote(notes_list)	
	    }).catch( function(result){	
	    	  console.log("Error occurred.");	
	      	  console.log(result);	
	});	
}

function upload(){
	var file = document.getElementById("upload").files[0]
	console.log(file);
	var name = $('#name').val().trim();

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

	console.log("upload successfull");
	document.getElementById("myModal").style.display = "none";
	document.getElementById("upload").val("");
	$('#name').val("");
	document.getElementById("uploadSubmit").disabled = true;
	
	s3.upload(params, function(err, data) {
		if(err){
			throw err;
		}
	})
}

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

function clearSearch(){
	table = document.getElementById("displaySearch");
	console.log(table.rows.length);
	var num = table.rows.length;
	for (var i = 1, row; i < num; i++){
		row = table.rows[1];
		table.deleteRow(1);
		console.log(i);
	}
}
