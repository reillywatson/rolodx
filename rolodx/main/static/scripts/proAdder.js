ProfessionalAdder = function() {
	this.init();
}

ProfessionalAdder.prototype = {
	
	element : null,
	
	constructor : ProfessionalAdder,
	
	init : function() {
		var template = "";
		template += "<div id='pro_placeholder'></div>";
		template += "<div id='pro_adder_container'>";
		template += "	<div id='pro_adder_top_label'>Can\'t Find The Person You're Looking For?</div>";
		template += "	<div id='pro_adder_bottom_label'>Add Them Now!</div>";
		template += "</div>";
		
		this.element = document.createElement("div");
		this.element.className = "pro_adder";
		this.element.innerHTML = template;
	},
	
	render : function( parent ) {
		parent.appendChild(this.element);
	}

};