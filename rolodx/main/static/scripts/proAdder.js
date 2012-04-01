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
		template += "	<div id='pro_adder_large_name' class='pro_adder_edit_text'>Name</div>";
		template += "	<div id='pro_adder_large_name_edit' class='gone'>"
		template += "		<input id='pro_adder_large_name_text' type='text' value='Name'></input>"
		template += "	</div>";
		template += "	<div id='pro_adder_large_category' class='pro_adder_edit_text'>Category</div>";
		template += "	<div id='pro_adder_large_category_edit' class='gone'>"
		template += "		<input id='pro_adder_large_category_text' type='text' value='Name'></input>"
		template += "	</div>";
		template += "	<div id='pro_adder_large_address' class='pro_adder_edit_text'>Address</div>";
		template += "	<div id='pro_adder_large_address_edit' class='gone'>"
		template += "		<input id='pro_adder_large_address_text' type='text' value='Name'></input>"
		template += "	</div>";
		template += "	<div id='pro_adder_large_phone' class='pro_adder_edit_text'>Phone Number</div>";
		template += "	<div id='pro_adder_large_phone_edit' class='gone'>"
		template += "		<input id='pro_adder_large_phone_text' type='text' value='Name'></input>"
		template += "	</div>";
		template += "	<div id='pro_adder_large_rating' class='pro_adder_edit_text'>Rating</div>";
		template += "	<div id='pro_adder_large_rating_edit' class='gone'>"
		template += "		<input id='pro_adder_large_rating_text' type='text' value='Name'></input>"
		template += "	</div>";
		template += "	<div id='pro_adder_large_review' class='pro_adder_edit_text'>Review</div>";
		template += "	<div id='pro_adder_large_review_edit' class='gone'>"
		template += "		<input id='pro_adder_large_review_text' type='text' value='Name'></input>"
		template += "	</div>";
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
		document.getElementById("pro_adder_large_name").onclick = this.editText;
		document.getElementById("pro_adder_large_name_text").onmouseout = this.onBlur;
		document.getElementById("pro_adder_large_category").onclick = this.editText;
		document.getElementById("pro_adder_large_category_text").onmouseout = this.onBlur;
		document.getElementById("pro_adder_large_address").onclick = this.editText;
		document.getElementById("pro_adder_large_address_text").onmouseout = this.onBlur;
		document.getElementById("pro_adder_large_phone").onclick = this.editText;
		document.getElementById("pro_adder_large_phone_text").onmouseout = this.onBlur;
		document.getElementById("pro_adder_large_rating").onclick = this.editText;
		document.getElementById("pro_adder_large_rating_text").onmouseout = this.onBlur;
		document.getElementById("pro_adder_large_review").onclick = this.editText;
		document.getElementById("pro_adder_large_review_text").onmouseout = this.onBlur	;
	},

	editText : function() {
		this.style.display = "none";
		document.getElementById(this.id+"_edit").className = "";
	},
	
	onBlur : function() {
		var display = document.getElementById(this.id.replace("_text", ""));
		var edit = document.getElementById(this.id.replace("_text", "_edit"));
		
		display.textContent = this.value;
		display.style.display = "block";
		display.className = "pro_adder_text";
		edit.className = "gone";
	},
};