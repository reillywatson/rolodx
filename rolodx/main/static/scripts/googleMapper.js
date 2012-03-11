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
		infoWindowContentTemplate += '<a href="/pro/{id}"';
		infoWindowContentTemplate += '	<div id="map_bubble_content">';
		infoWindowContentTemplate += '		<div class="map_bubble_name">{name}</div>';
		if (data.averageRating != 0) {
		infoWindowContentTemplate += '		<div class="map_bubble_rating">';
		infoWindowContentTemplate += '			<div class="rating_stars_{stars}"></div>';
		infoWindowContentTemplate += '			<div class="map_bubble_num_ratings">({numRatings})</div>';
		infoWindowContentTemplate += '		</div>';
		}
		infoWindowContentTemplate += '	</div>';
		infoWindowContentTemplate += '</a>';
		var infoWindowContent = infoWindowContentTemplate.
				replace(/{id}/, data.id).
				replace(/{name}/, data.name).
				replace(/{stars}/, data.averageRating).
				replace(/{numRatings}/,data.numRatings);

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
	
	renderMarkers : function(bounds) {
		var that = this;
		
		for (var i=0; i< this.markers.length; i++) {
			var marker = this.markers[i];
			marker.setMap(this.map);
			if (bounds) {
				bounds.extend(marker.position);
			}
			
			// I'm gonna be tricky, here.
			//	I'll keep a reference to the current GoogleMapper object in 'that'
			//	When I'm inside my "clicked" function, I'll get the global infoWindow from 'that', and my data from 'this' (which is the current marker clicked)
			// 	I can't use "marker" because that's gonna be whatever the last value of 'marker' was.
			google.maps.event.addListener(marker, 'click', function() {
				that.infoWindow.setContent(this.content);
				that.infoWindow.open(this.map,this);
			});
		}
	},
	
	render : function( container ) {
		this.container = document.getElementById(container);
		this.map = new google.maps.Map(this.container, this.options);
		
		var that = this;
		var bounds = new google.maps.LatLngBounds();
		this.renderMarkers(bounds);
		
		// Set a reasonable zoom level, if fit bounds finds a single entry
		// Has to happen like this, because fitBounds is async, so we don't know the zoom level right away
		var listener = google.maps.event.addListenerOnce(this.map, 'zoom_changed', function() {
			zoomChangeBoundsListener = google.maps.event.addListenerOnce(that.map, 'bounds_changed', function(event) 
			{
				if (this.getZoom() > that.MIN_DEFAULT_ZOOM_LVL) {
					this.setZoom(that.MIN_DEFAULT_ZOOM_LVL);
				}
			});
		});
		
		if (this.markers.length > 0) {
			this.map.fitBounds(bounds)
		}
	},
	
	addMoveListener : function( fn ) {
		var that = this;
		google.maps.event.addListenerOnce( this.map, 'idle', function() {
			google.maps.event.addListener( that.map, 'bounds_changed', function() {
				var bounds = this.getBounds();
				var center = bounds.getCenter();
				var ne = bounds.getNorthEast();
				var sw = bounds.getSouthWest();

				// r = radius of the earth in statute miles
				var r = 3963.0;  

				// Convert lat or lng from decimal degrees into radians (divide by 57.2958)
				var lat1 = center.lat() / 57.2958; 
				var lon1 = center.lng() / 57.2958;
				var lat2 = ne.lat() / 57.2958;
				var lon2 = ne.lng() / 57.2958;

				// distance = circle radius from center to Northeast corner of bounds
				var dis = r * Math.acos(Math.sin(lat1) * Math.sin(lat2) + 
				  Math.cos(lat1) * Math.cos(lat2) * Math.cos(lon2 - lon1));
			
				fn( dis, ne, sw );
			});
		});
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
			if (that.container.className == "map_canvas") {
				that.container.className = "map_canvas_full";
				this.firstChild.data = "Shrink Map...";
			} else {
				that.container.className = "map_canvas";
				this.firstChild.data = "Expand Map...";
			}
			
			var center = that.map.getCenter();			
			google.maps.event.trigger(that.map, "resize");
			that.map.setCenter(center);
		}
	}
}
