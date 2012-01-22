GoogleMapper = function( data ) {
	this.init(data)
}

GoogleMapper.prototype = {
	
	// Default map location to Toronto
	center : new google.maps.LatLng(43.716589,-79.340686),
	
	options : null,
	
	markers : [],
	
	infoWindow : null,
	
	selected : 0,
	
	init : function( data ) {
		this.options = {
			center: this.center,
			zoom: 11,
			disableDefaultUI: true,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};		
		
		this.infoWindow = new google.maps.InfoWindow({
			maxWidth: 200
		});
	},
	
	addMarker : function( data, index ) {
		if (!data.address_latitude) {
			return;
		}
		var imageOn = "../static/images/marker_on.png";
		var imageOff = "../static/images/marker_off.png";
		
		var infoWindowContentTemplate  = '';
		infoWindowContentTemplate += '<div id="map_bubble_content">';
		infoWindowContentTemplate += '	<div class="map_bubble_name">{name}</div>';
		if (data.averageRating != 0) {
		infoWindowContentTemplate += '	<div class="map_bubble_rating">';
		infoWindowContentTemplate += '		<div class="rating_stars_{stars}"></div>';
		infoWindowContentTemplate += '		<div class="map_bubble_num_ratings">({numRatings})</div>';
		infoWindowContentTemplate += '	</div>';
		}
		infoWindowContentTemplate += '</div>';
		var infoWindowContent = infoWindowContentTemplate.replace(/{name}/, data.name).replace(/{stars}/, data.averageRating).replace(/{numRatings}/,data.numRatings);

		// NOTE: 'content' isn't an existing attribute. But it'll be added for me, and it'll hold the infoWindow content for later. 
		// This is so that I can use a single infoWindow object, instead of n (which is easier and faster).
		var marker = new google.maps.Marker({
			position: new google.maps.LatLng(data.address_latitude, data.address_longitude),
			title: data.name,
			content: infoWindowContent,
			icon: index == this.selected? imageOn : imageOff
		});
		
		this.markers.push(marker);
	},
	
	render : function( parent ) {
		var map = new google.maps.Map(document.getElementById(parent), this.options);
		var bounds = new google.maps.LatLngBounds();
		for (var i=0; i< this.markers.length; i++) {
			var marker = this.markers[i];
			marker.setMap(map);
			bounds.extend(marker.position);
			// I'm gonna be tricky, here.
			//	I'll keep a reference to the current GoogleMapper object in 'that'
			//	When I'm inside my "clicked" function, I'll get the global infoWindow from 'that', and my data from 'this' (which is the current marker clicked)
			// 	I can't use "marker" because that's gonna be whatever the last value of 'marker' was.
			var that = this;
			google.maps.event.addListener(marker, 'click', function() {
				that.infoWindow.setContent(this.content);
				that.infoWindow.open(map,this);
			});
		}
		map.fitBounds(bounds)
	},
	
	setSelected : function (selection) {
		var imageOn = "../static/images/marker_on.png";
		var imageOff = "../static/images/marker_off.png";
		
		// Unset the previously selected marker
		this.markers[this.selected].setIcon(imageOff);
		
		// Set the new marker
		this.selected = selection;
		this.markers[selection].setIcon(imageOn);
	}
}
