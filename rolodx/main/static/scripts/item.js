Review = function (  review  ) {
	this.init(review)
};

Review.prototype = {
	
	author : null,
	
	rating : 0,
	
	text : null,
    
    constructor : Review,
	
	init : function( review ) {
		function starsNumToString(num) {
			var rounded = Math.round(num* 2) / 2;
			return (rounded == 0 ) ? "0_5" : rounded.toString().replace(/\./,'_');
		}
		
		this.rating = starsNumToString(review.rating);
		this.author = review.author;
		this.text = review.text;
		
		
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