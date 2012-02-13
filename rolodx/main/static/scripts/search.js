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
	
	render : function ( parent ) {
		parent.appendChild(this.element);
	},
	
	addMouseOver : function( i, mapper ) {
		this.element.onmouseover = function(event) { mapper.setSelected(i); };
	}
}

SearchPaginator = function( data ) {
	this.init(data)
}

SearchPaginator.prototype = {
	PAGE : "Page {page} of {numPages}",	
	template : "",
	constructor : SearchPaginator,
	init : function( data ) {
		var currentPage = data.paging.currentPage;
		var numPages = data.paging.numPages;
		var currentUrl = document.location.href.replace('&p='+currentPage, '')
		
		if (currentPage > 1) {
			this.template += "<a class='pager_white' href='"+currentUrl+"&p=1'>&lt;&lt;</a>"
			this.template += "<a class='pager_white' href='"+currentUrl+"&p=" + (currentPage-1) + "'>&lt;</a>"
		}
		
		this.template += "&nbsp;<span> " + this.PAGE.replace(/{page}/,currentPage).replace(/{numPages}/,numPages) + "</span>&nbsp;"
		
		if (currentPage < numPages) {
			this.template += "<a class='pager_white' href='"+currentUrl+"&p=" + (currentPage+1) + "'>&gt;</a>"
			this.template += "<a class='pager_white' href='"+currentUrl+"&p=" + (numPages) + "'>&gt;&gt;</a>"
		}
	},
	
	render : function( elementId ) {
		parent = document.getElementById(elementId);
		parent.innerHTML += this.template;
	}
}
	
