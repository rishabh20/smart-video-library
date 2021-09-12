var global_userID;
var global_video;

// $(document).ready(function(){
// 	global_userID = "";
// 	global_video = "";
// });

function saveVideo(video){
	global_video = video;
	sessionStorage.setItem("global_video", video)
}

function getVideo(){
	return sessionStorage.getItem("global_video");
}

function setID(id){
	global_userID = id;
	sessionStorage.setItem("global_userID", id);
}

function getID(){
	return sessionStorage.getItem("global_userID");
}