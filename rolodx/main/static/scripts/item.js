Item = function ( data ) {
	this.init(data);
};

Item.prototype = {
	
	name : null,
	
	job : null,
	
	rating : null,
	
	numRatings : null,
	
	address : null,
	
	website : null,
	
	email : null,
	
	hours : null,
	
	description : null,
	
	icon: null,
	
	constructor : Item,
	
	init : function( data ) {		
		function starsNumToString(num) {
			var rounded = Math.round(num* 2) / 2;
			return (rounded == 0 ) ? "0_5" : rounded.toString().replace(/\./,'_');
		}
		
		this.rating = starsNumToString(data.rating);
		this.numRatings = data.numRatings;
		this.name = data.name;
		this.job = data.job;
		this.address = data.address;
		this.website = data.website;
		this.email = data.email;
		this.hours = data.hours;
		this.description = data.description;
		this.icon = data.icon;
	},
	
	render : function () {
		document.getElementById("item_metadata_icon");
		document.getElementById("item_metadata_name").innerHTML = this.name;
		document.getElementById("item_metadata_job").innerHTML = this.job;
		document.getElementById("item_metadata_rating_stars").className = "rating_stars_" + this.rating;
		document.getElementById("item_metadata_num_ratings").innerHTML = "(" + this.numRatings + ")";
		document.getElementById("item_metadata_address").innerHTML = this.address;
		document.getElementById("item_metadata_web").innerHTML = "Web: " + this.website;
		document.getElementById("item_metadata_contact").innerHTML = "Contact: " + this.email;
		document.getElementById("item_metadata_hours").innerHTML = "Hours: " + this.hours;
		document.getElementById("item_metadata_description").innerHTML = this.description;
	},
	
	toString : function() {
		return this.name;
	}
}

/**********************/
/**		REVIEW		**/

Review = function (  data  ) {
	this.init(data)
};

Review.prototype = {
	
	author : null,
	
	rating : null,
	
	text : null,
    
    constructor : Review,
	
	init : function( data ) {
		function starsNumToString(num) {
			var rounded = Math.round(num* 2) / 2;
			return (rounded == 0 ) ? "0_5" : rounded.toString().replace(/\./,'_');
		}
		
		this.rating = starsNumToString(data.rating);
		this.author = data.author;
		this.text = data.text;
		
		
	},
	
	render : function( parent ) {
        var template = "";
		template +=	'<div class="item_review">';
		template +=		'<div class="rating_stars_{stars}"></div>';
		template +=		'<div class="item_review_text">{text}</div>';
		template +=		'<div class="item_review_author">- {author}</div>';
		template +=	'</div>';
		
		template = template.replace(/{stars}/,this.rating);
		template = template.replace(/{text}/,this.text);
		template = template.replace(/{author}/,this.author);
		
		parent.innerHTML += template
	},
	
	toString : function() {
		return "author: " +this.author + " rating " + this.rating + " text " + this.text; 
	}
	
};