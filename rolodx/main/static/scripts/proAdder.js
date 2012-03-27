ProfessionalAdder = function() {
	this.init();
}

ProfessionalAdder.prototype = {
	
	smallElement : null,
	
	largeElement : null,
	
	element : null,
	
	constructor : ProfessionalAdder,
	
	init : function() {
		var template = "";
		template += "<div id='pro_adder_small_icon'></div>";
		template += "<div id='pro_adder_small_container'>";
		template += "	<div id='pro_adder_small_top_label'>Can\'t Find The Person You're Looking For?</div>";
		template += "	<div id='pro_adder_small_bottom_label'>Add Them Now!</div>";
		template += "</div>";
		this.smallElement = document.createElement("div");
		this.smallElement.className = "pro_adder_small";
		this.smallElement.innerHTML += template;
		
		template  = "<div id='pro_adder_large_icon'></div>";
		template += "<div id='pro_adder_large_container'>";
		template += "	<div id='pro_adder_large_name' class='pro_adder_large_txt'>Name</div>";
		template += "	<div id='pro_adder_large_category' class='pro_adder_large_txt'>Category</div>";
		template += "	<div id='pro_adder_large_address' class='pro_adder_large_txt'>Address</div>";
		template += "	<div id='pro_adder_large_phone' class='pro_adder_large_txt'>Phone Number</div>";
		template += "	<div id='pro_adder_large_rating' class='pro_adder_large_txt'>Rating</div>";
		template += "	<div id='pro_adder_large_review' class='pro_adder_large_txt'>Review</div>";
		template += "</div>";
		this.largeElement = document.createElement("div");
		this.largeElement.className = "pro_adder_large gone";
		this.largeElement.innerHTML += template;
		
		var that = this;
		this.smallElement.onclick = function() {
			that.smallElement.className = "gone";
			that.largeElement.className = "pro_adder_large";
		}
		
		this.element = document.createElement("div");
		this.element.className = "pro_adder";
		this.element.appendChild( this.smallElement );
		this.element.appendChild( this.largeElement );
	},
	
	render : function( parent ) {
		parent.appendChild(this.element);
	}

};