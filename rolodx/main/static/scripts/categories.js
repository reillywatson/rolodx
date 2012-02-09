"use strict";

function Category( data ) {
	this.init(data);
}

Category.prototype = {
	CSS : "subcategories_item",

	label : "",
	
	element : null,
	
	constructor : Category,
	
	init : function( data ) {
		this.label = data;
		
		var template = "<div class='" + this.CSS + "'>" + this.label + "</div>";
		
		this.element = document.createElement("a");
		this.element.href = "/category/" + this.label;
		this.element.innerHTML = template;
	},
	
	render : function( parent ) {
		parent.appendChild(this.element);
	}
};

/** STATIC **/
Category.initializeSet = function( dataArray ) {
	var result = [];
	for (var i in dataArray) {
		result.push(new Category(dataArray[i]));
	}
	return result;
}