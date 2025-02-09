// TODO: This needs to be pulled out and re-used on the Search pages.
Professional = function( data ) {
	this.init(data);
}

Professional.prototype = {
	id : null,
	
	icon : null,
	
	name : null, 
	
	occupation : null,
	
	rating : null,
	
	numRatings : null,
	
	description : null,
	
	constructor : Professional,
	
	element : null,
	
	content : "",
	
	init : function( resultData ) {
		function starsNumToString(num) {
			var rounded = Math.round(num* 2) / 2;
			return rounded.toString().replace(/\./,'_');
		}
		this.rating = starsNumToString(resultData.averageRating);
		this.id = resultData.id;
		this.icon = resultData.icon;
		this.name = resultData.name;
		this.occupation = resultData.occupation;
		this.description = resultData.description;
		this.numRatings = resultData.numRatings;
		
		var template = "";
		template += "	<a class='no-link' href='/pro/{id}'>";
		template +="		<img class='pro_icon'></img>";
		template +="		<div class='pro_text'>{name},&nbsp;{occupation}</div>";
		template +="		<div class='pro_description'>{description}</div>";
		if (resultData.averageRating != 0) {
		template +="		<div class='pro_rating'>";
		template +="			<div class='rating_stars_{stars}'></div>";
		template +="			<div class='num_ratings'>({num_ratings})</div>";
		template +="		</div>";
		}
		template +="	</a>";
		
		template = template.replace(/{id}/,this.id);
		template = template.replace(/{name}/,this.name);
		template = template.replace(/{occupation}/,this.occupation);
		template = template.replace(/{description}/, (this.description ? this.description : ""));
		template = template.replace(/{stars}/,this.rating);
		template = template.replace(/{num_ratings}/,this.numRatings);
		
		this.element = document.createElement("div");
		this.element.className = "pro_container";
		this.element.innerHTML = template;
	},
	
	render : function ( elementId ) {
		var parent = document.getElementById(elementId);
		parent.appendChild(this.element);
	},
};

Profile = function( data ) {
	this.init(data);
}

Profile.prototype = {
	
	name : "",
	
	email : "",
	
	template : "",
	
	constructor : Profile,
	
	init : function(data) {
		this.name = data.name;
		this.email = data.email;
		
		this.template += "<div id='profile_photo' class='pro_icon'></div>";
		this.template += "<div id='profile_data_group'>";
		this.template += "	<div id='profile_name'>" + this.name + "</div>";
		this.template += "	<div id='profile_fb_email'>"+ this.email +"</div>";
		this.template += "	<div id='profile_badges'>TODO: User Badges a-la Stack Overflow</div>";
		this.template += "</div>";
	},
	
	render : function( elementId ) {
		var parent = document.getElementById(elementId);
		parent.innerHTML = this.template;
	},
	
};