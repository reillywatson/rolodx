SearchResult = function( resultData ) {
	this.init(resultData);
}

SearchResult.prototype = {
	
	id : null,
	
	icon : null,
	
	name : null, 
	
	occupation : null,
	
	rating : null,
	
	numRatings : null,
	
	description : null,
	
	constructor : SearchResult,
	
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
		template +="<div class='pro_container'>";
		template += "	<a class='no-link' href='/pro/{id}'>";
		template +="		<img class='pro_icon'></img>";
		template +="		<div class='pro_text'>{name},&nbsp;{occupation}</div>";
		template +="		<div class='pro_description'>{description}</div>"
		if (resultData.averageRating != 0) {
		template +="		<div class='pro_rating'>"
		template +="			<div class='rating_stars_{stars}'></div>"
		template +="			<div class='num_ratings'>({num_ratings})</div>"
		template +="		</div>"
		}
		template +="	</a>"
		template +="</div>"
		
		template = template.replace(/{id}/,this.id);
		template = template.replace(/{name}/,this.name);
		template = template.replace(/{occupation}/,this.occupation);
		template = template.replace(/{description}/, (this.description ? this.description : ""));
		template = template.replace(/{stars}/,this.rating);
		template = template.replace(/{num_ratings}/,this.numRatings);
		
		this.content = template;
	},
	
	render : function ( parent ) {
		parent.innerHTML += this.content;
	}

}
	