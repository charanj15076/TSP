import { Component, ElementRef } from '@angular/core';
import { formatDate } from '@angular/common';
import { LoadingController, Platform, ToastController } from '@ionic/angular';
import { Geolocation } from '@capacitor/geolocation';
import { RoutesService } from 'src/services/routes.service';

import * as L from "leaflet";


@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})

export class HomePage {
  // this latlng is used for viewport centering and navigation
  initLat = 0;
  initLng = 0;

  myMap: L.Map | undefined;

  locationIcon = L.divIcon({
    className: "location-marker",
    html: `<ion-icon name="location"/>`,

    iconAnchor: [20, 40],
    iconSize: [40, 40],
    popupAnchor: [0, -40] // point from which the popup should open relative to the iconAnchor
  });


  // this latlng is for marking the map
  focusLocationExists: boolean = false;
  focusLocationMark: L.Marker | undefined;
  focusLocationLat: any;
  focusLocationLng: any;


  polylines: any[] = [];
  destinations: any[] = [];
  destinationsMarks: any[] = [];

  constructor(
    private loadingCtrl: LoadingController,
    private routesService: RoutesService,
    private elementRef: ElementRef,
    private toastController: ToastController,
    public platform: Platform
  ) {}

  ionViewDidEnter() {
    this.loadMap();
  }

  // search item was clicked
  onsSearchResultSelected(selectedItem : any) {
    this.focusLocationLat = selectedItem.y;
    this.focusLocationLng = selectedItem.x;

    // pan to coordinates and drop a marker
    this.myMap?.setView([this.focusLocationLat, this.focusLocationLng], this.myMap.getZoom(), {
      animate: true,
      duration: 1,
      easeLinearity: 0.25
    });

    if (this.focusLocationMark) this.myMap?.removeLayer(this.focusLocationMark);
    this.focusLocationMark = L.marker([this.focusLocationLat, this.focusLocationLng], { icon: this.locationIcon }).addTo(this.myMap!);
  }

  // check if focusLocation has values
  hasFocusLocation() {
    if (this.focusLocationMark === undefined) return false;
    else return true;
  }

  // on initial load, load the map
  async loadMap() {
    let coordinates: any;
    if (!this.platform.is('cordova')) {
      const getCoords = async () => {
        const pos = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject);
        });
        return pos;
      };
      coordinates = await getCoords();
    } else {
      console.log('there');
      coordinates = await Geolocation.getCurrentPosition();
    }
    // console.log('Current position:', coordinates);

    this.initLat = coordinates.coords.latitude;
    this.initLng = coordinates.coords.longitude;

    this.myMap = L.map('map', {
      maxZoom: 18,
      minZoom: 8,
      zoomControl: false
    }).setView([this.initLat, this.initLng], 15);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(this.myMap);

    L.control.zoom({
      position: 'bottomleft'
    }).addTo(this.myMap);

    // allow marker drop on click around the map area
    this.myMap.on("click", e => {
      this.focusLocationLat = e.latlng.lat;
      this.focusLocationLng = e.latlng.lng;
      if (this.focusLocationMark) this.myMap?.removeLayer(this.focusLocationMark);
      this.focusLocationMark = L.marker([this.focusLocationLat, this.focusLocationLng], { icon: this.locationIcon }).addTo(this.myMap!); 
    });
  }

  // set map view to current location
  async viewCurrentLocation() {
    this.presentToast('Centering viewport around current location.', 'warning')

    let coordinates: any;
    if (!this.platform.is('cordova')) {
      const getCoords = async () => {
        const pos = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject);
        });
        return pos;
      };
      coordinates = await getCoords();
    } else {
      coordinates = await Geolocation.getCurrentPosition();
    }

    this.initLat = coordinates.coords.latitude;
    this.initLng = coordinates.coords.longitude;

    this.myMap?.setView([this.initLat, this.initLng], this.myMap.getZoom(), {
      animate: true,
      duration: 1,
      easeLinearity: 0.25
    });
  }

  async viewLocation(lat: any, lng: any) {
    this.myMap?.setView([lat, lng], this.myMap.getZoom(), {
      animate: true,
      duration: 1,
      easeLinearity: 0.25
    });
  }

  // add a destination
  addDestination() {
    if (this.focusLocationMark == undefined) {
      this.presentToast('Please select a destination.', 'warning');
      return;
    }

    // get latlng details
    var lat = this.focusLocationLat;
    var lng = this.focusLocationLng;

    // remove the mark so we can turn it to a destination icon
    this.myMap?.removeLayer(this.focusLocationMark!);
    this.focusLocationMark = undefined;

    // prepare onclick behavior
    // set marker of the new blockage
    const popupContents = `
      Lat: ${lat}
      <br> Long: ${lng}
      <br> <button class="delete">Remove Destination</button>
    `;

    // add marker
    let marker : any = L.marker([lat, lng], { icon: this.locationIcon })
                    .bindPopup(popupContents, { className: "marker-popup" })
    marker.addTo(this.myMap!)._icon.classList.add('routing-destination');


    // marker click behavior
    marker.on('popupopen', () => {
      this.myMap?.setView([lat, lng], this.myMap.getZoom(), {
        animate: true,
        duration: 1,
        easeLinearity: 0.25
      });

      [...this.elementRef.nativeElement.querySelectorAll('.delete')].pop()
        .addEventListener('click', () => {
          this.removeDestination(marker);
          this.myMap?.closePopup();
        });
    });

    this.destinations.push([lat, lng]);
    this.destinationsMarks.push(marker);

    this.presentToast('Destination added.', 'success');
    console.log(this.destinations)
  }

  // remove a destination
  removeDestination(marker: any) {
    var destIdx = this.destinationsMarks.indexOf(marker);
    if (destIdx > -1) {
      this.destinations.splice(destIdx, 1);
      this.destinationsMarks.splice(destIdx, 1);
      this.myMap?.removeLayer(marker!);
    }
    this.presentToast('Destination removed.', 'success');
    console.log(this.destinations)
  }

  removeDestinationIdx(idx: any) {
    this.myMap?.removeLayer(this.destinationsMarks[idx]!);
    this.destinations.splice(idx, 1);
    this.destinationsMarks.splice(idx, 1);

    this.presentToast('Destination removed.', 'success');
    console.log(this.destinations)
  }

  // remove all destination markers
  removeAllDestinations() {
    this.clearMapLines();

    this.destinationsMarks.forEach( (marker: any) => {
      this.myMap?.removeLayer(marker!);
    })
    this.destinations = [];
    this.destinationsMarks = [];

    this.presentToast('Removed all the elements from the map.', 'success');
  }

  clearMapLines() {
    this.polylines.forEach( (polyline: any) => {
      this.myMap?.removeLayer(polyline);
    })
    this.polylines = [];
  }

  tspSolution: any = {}
  solveTSP(technique: string) {
    this.clearMapLines();

    let postData = {
      destinationList: this.destinations,
      technique: technique,
    }

    this.routesService.runTSP(postData).subscribe( (res) => {
      console.log(res);
      this.tspSolution = {
        routes: JSON.parse(res.data.routes),
      }

      this.tspSolution.routes.features.forEach( (elem: any) => {
        var pl = L.polyline(
          L.GeoJSON.coordsToLatLngs(elem.geometry.coordinates, 0), {
            color: 'red'
          }).addTo(this.myMap!);
        this.polylines.push(pl);
      });
    });
  }

  async presentToast(message: string, color: string) {
    const toast = await this.toastController.create({
      message: message,
      duration: 2000,
      position: 'top',
      color: color,
      cssClass: 'toast-notification',
    });

    await toast.present();
  }
}
