GoogleMapper = function( data ) {
	this.init(data)
}

GoogleMapper.prototype = {
	
	IMAGE_ON : "../static/images/marker_on.png",
	
	IMAGE_OFF: "../static/images/marker_off.png",
	
	MIN_DEFAULT_ZOOM_LVL: 14,
	
	// Default map location to Toronto
	center : new google.maps.LatLng(43.716589,-79.340686),
	
	options : null,
	
	markers : [],
	
	infoWindow : null,
	
	selected : 0,
	
	container : null,
	
	map : null,
	
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
			icon: index == this.selected? this.IMAGE_ON : this.IMAGE_OFF
		});
		
		this.markers.push(marker);
	},
	
	render : function( container ) {
		this.container = document.getElementById(container);
		this.map = new google.maps.Map(this.container, this.options);
		
		var bounds = new google.maps.LatLngBounds();
		var that = this;
		
		for (var i=0; i< this.markers.length; i++) {
			var marker = this.markers[i];
			marker.setMap(this.map);
			bounds.extend(marker.position);
			// I'm gonna be tricky, here.
			//	I'll keep a reference to the current GoogleMapper object in 'that'
			//	When I'm inside my "clicked" function, I'll get the global infoWindow from 'that', and my data from 'this' (which is the current marker clicked)
			// 	I can't use "marker" because that's gonna be whatever the last value of 'marker' was.
			google.maps.event.addListener(marker, 'click', function() {
				that.infoWindow.setContent(this.content);
				that.infoWindow.open(this.map,this);
			});
		}
		
		// Set a reasonable zoom level, if fit bounds finds a single entry
		// Has to happen like this, because fitBounds is async, so we don't know the zoom level right away
		google.maps.event.addListener(this.map, 'zoom_changed', function() {
			zoomChangeBoundsListener = google.maps.event.addListener(that.map, 'bounds_changed', function(event) 
			{
				if (this.getZoom() > that.MIN_DEFAULT_ZOOM_LVL) {
					this.setZoom(that.MIN_DEFAULT_ZOOM_LVL);
				}

				// Make sure this only happens on the initial page load
				google.maps.event.clearListeners(that.map, 'zoom_changed');
				google.maps.event.clearListeners(that.map, 'bounds_changed');
			});
		});
		
		if (this.markers.length > 0) {
			this.map.fitBounds(bounds)
		}
	},
	
	setSelected : function (selection) {
		if (selection >= this.markers.length) return;
		
		// Unset the previously selected marker
		this.markers[this.selected].setIcon(this.IMAGE_OFF);
		
		// Set the new marker
		this.selected = selection;
		this.markers[selection].setIcon(this.IMAGE_ON);
	},
	
	setExpandTrigger : function( id ) {
		var trigger = document.getElementById(id);
		var that = this;
		trigger.onclick = function() {
			var oldClass = that.container.className;
			that.container.className = oldClass == "map_canvas"? "map_canvas_full" : "map_canvas";
			var center = that.map.getCenter();
			
			google.maps.event.trigger(that.map, "resize");
			that.map.setCenter(center);
		}
	}
}
