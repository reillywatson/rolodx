Item = function ( data ) {
	this.init(data);
};

Item.prototype = {
	
	name : null,
	occupation : null,
	rating : null,
	numRatings : null,
	street_address : null,
	website : null,
	email : null,
	hours : null,
	description : null,
	icon: null,
	constructor : Item,
	
	init : function( data ) {		
		function starsNumToString(num) {
			var rounded = Math.round(num* 2) / 2;
			return rounded.toString().replace(/\./,'_');
		}
		
		this.rating = starsNumToString(data.averageRating);
		this.numRatings = data.numRatings;
		this.name = data.name;
		this.occupation = data.occupation;
		this.street_address = data.street_address;
		this.website = data.website;
		this.email = data.email;
		this.hours = data.hours;
		this.description = data.description;
		this.icon = data.icon;
	},
	
	render : function () {
		document.getElementById("item_metadata_icon");
		document.getElementById("item_metadata_name").innerHTML = this.name;
		document.getElementById("item_metadata_job").innerHTML = this.occupation;
		document.getElementById("item_metadata_rating_stars").className = "rating_stars_" + this.rating;
		document.getElementById("item_metadata_num_ratings").innerHTML = "(" + this.numRatings + ")";
		document.getElementById("item_metadata_address").innerHTML = this.street_address;
		document.getElementById("item_metadata_web").innerHTML = "Web: " + this.website;
		document.getElementById("item_metadata_contact").innerHTML = "Contact: " + this.email;
		document.getElementById("item_metadata_hours").innerHTML = "Hours: " + this.hours;
		document.getElementById("item_metadata_description").innerHTML = this.description;
	},
	
	toString : function() {
		return this.name;
	}
}

var currentStarCount = null;
starOut = function() {
	starHover(currentStarCount || 0);
}

starHover = function(numStars) {
	for (var i = 1; i <= 5; i++) {
		var starItem = document.getElementById('item_star_'+i);
		if (i <= numStars) {
			starItem.style.backgroundImage="url('../static/images/star.png')";
		}
		else {
			starItem.style.backgroundImage="url('../static/images/star_empty.png')";
		}
	}
};

starClick = function(numStars) {
	currentStarCount = numStars;
};

addReview = function() {
	var reviewText = document.getElementById("review_text").value;
	var rating = currentStarCount;
	var userDisplayName = 'some test user';
	var userId = '1';
	data = {userDisplayName:userDisplayName, userId:userId, rating:rating, text:reviewText};
	var review = new Review(data);
	var parentElementReviews = document.getElementById('item_reviews');
	var addReviewUrl = document.location.href.split('?')[0] + '/addReview'
	YUI().use(["cookie","io-base"], function(Y) {
		// TODO: add a callback here hooked up to a spinner or something
		var headers = {"X-CSRFToken": Y.Cookie.get('csrftoken'), 'Content-Type':'application/json'};
		Y.io(addReviewUrl, {method:"POST", data:data, headers:headers});
	});
	review.render(parentElementReviews);
};


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
	content : "",
	
	init : function( data ) {
		function starsNumToString(num) {
			var rounded = Math.round(num* 2) / 2;
			return (rounded == 0 ) ? "0_5" : rounded.toString().replace(/\./,'_');
		}
		this.rating = starsNumToString(data.rating);
		this.author = data.user.fields.username;
		this.text = data.text;
		
        var template = "";
		template +=	'<div class="item_review">';
		template +=		'<div class="rating_stars_{stars}"></div>';
		template +=		'<div class="item_review_text">{text}</div>';
		template +=		'<div class="item_review_author">- {author}</div>';
		template +=	'</div>';
		
		template = template.replace(/{stars}/,this.rating);
		template = template.replace(/{text}/,this.text);
		template = template.replace(/{author}/,this.author);
		
		this.content = template;
	},
	
	render : function( parent ) {
		parent.innerHTML += this.content
	},
	
	toString : function() {
		return "author: " +this.author + " rating " + this.rating + " text " + this.text; 
	}
};

Paginator = function( data ) {
	this.init(data);
}

Paginator.prototype = {
	NO_REVIEWS_YET : "No Reviews Yet",
	PAGE : "Page {page} of {numPages}",
	currentPage : 1,
	numPages : 1,
	constructor : Paginator,
	template : "",
	
	init : function( data ) {
		this.currentPage = data.currentPage;
		this.numPages = data.numPages;
		
		if (this.currentPage > 1) {
			this.template += "<a class='pager_black' href='?p=1'>&lt;&lt;</a>"
			this.template += "<a class='pager_black' href='?p=" + (this.currentPage-1) + "'>&lt;</a>"
		}
		
		if (this.currentPage == 1 && this.numPages == 1) {
			this.template += "<span> " + this.NO_REVIEWS_YET + " </span>"
		} else {
			this.template += "<span> " + this.PAGE.replace(/{page}/,this.currentPage).replace(/{numPages}/,this.numPages) + "</span>"
		}
		
		if (this.currentPage < this.numPages) {
			this.template += "<a class='pager_black' href='?p=" + (this.currentPage+1) + "'>&gt;</a>"
			this.template += "<a class='pager_black' href='?p=" + this.numPages + "'>&gt;&gt;</a>"
		}
	},
	
	render : function( elementId ) {
		parent = document.getElementById(elementId);
		parent.innerHTML += this.template;
	}
}
