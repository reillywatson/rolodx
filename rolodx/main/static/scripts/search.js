SearchResult = function( resultData ) {
	this.init(resultData);
}

SearchResult.prototype = {
	
	icon : null,
	
	name : null, 
	
	occupation : null,
	
	rating : null,
	
	description : null,
	
	constructor : SearchResult,
	
	content : "",
	
	init : function( resultData ) {
		function starsNumToString(num) {
			var rounded = Math.round(num* 2) / 2;
			return (rounded == 0 ) ? "0_5" : rounded.toString().replace(/\./,'_');
		}
		this.rating = starsNumToString(resultData.rating);
		this.icon = resultData.icon;
		this.name = resultData.name;
		this.occupation = resultData.occupation;
		this.description = resultData.description;
		
		var template = "";
		template +="<div class='pro_container'>";
		template += "	<a class='no-link' href='/pro/proId'>";
		template +="		<img class='pro_icon'></img>";
		template +="		<div class='pro_text'>{name}</div>";
		template +="		<div class='pro_text'>{occupation}</div>";
		template +="		<div class='pro_text'>"
		template +="			<div class='pro_rating'>Rating:</div>"
		template +="			<div class='rating_stars_{stars}'></div>"
		template +="		</div>"
		template +="		<div class='pro_description'>{description}</div>"
		template +="		<div class='pro_separator'></div>"
		template +="	</a>"
		template +="</div>"
		
		template = template.replace(/{name}/,this.name);
		template = template.replace(/{occupation}/,this.occupation);
		template = template.replace(/{description}/, (this.description ? this.description : ""));
		template = template.replace(/{stars}/,this.rating);
		
		this.content = template;
	},
	
	render : function ( parent ) {
		parent.innerHTML += this.content;
	}

}
	