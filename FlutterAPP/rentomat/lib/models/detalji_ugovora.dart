class Svidetalji {
  int? count;
  List<Results>? results;

  Svidetalji({this.results});

  Svidetalji.fromJson(Map<String, dynamic> json) {
    count = json['count'];
    if (json['results'] != null) {
      results = <Results>[];
      json['results'].forEach((v) {
        results!.add(new Results.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['count'] = this.count;
    if (this.results != null) {
      data['results'] = this.results!.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class Results {
  int? id;
  String? name;
  String? rentStartDate;
  String? rentEndDate;
  VehicleId? vehicleId;
  RentFrom? rentFrom;
  CustomerId? customerId;

  Results(
      {this.id,
      this.name,
      this.rentStartDate,
      this.rentEndDate,
      this.vehicleId,
      this.rentFrom,
      this.customerId});

  Results.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    name = json['name'];
    rentStartDate = json['date_start'];
    rentEndDate = json['date_end'];
    vehicleId = json['vehicle_id'] != null
        ? new VehicleId.fromJson(json['vehicle_id'])
        : null;
    rentFrom = json['rent_from'] != null
        ? new RentFrom.fromJson(json['rent_from'])
        : null;
    customerId = json['tenant_id'] != null
        ? new CustomerId.fromJson(json['tenant_id'])
        : null;
  }

  //get rent_start_date => null;

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['name'] = this.name;
    data['date_start'] = this.rentStartDate;
    data['date_end'] = this.rentEndDate;
    if (this.vehicleId != null) {
      data['vehicle_id'] = this.vehicleId!.toJson();
    }
    if (this.rentFrom != null) {
      data['rent_from'] = this.rentFrom!.toJson();
    }
    if (this.customerId != null) {
      data['tenant_id'] = this.customerId!.toJson();
    }
    return data;
  }
}

class VehicleId {
  String? name;
  String? licensePlate;
  String? keyPosition;
  XBaznaLokacija? xBaznaLokacija;
  XTrenutnaLokacija? xTrenutnaLokacija;

  VehicleId(
      {this.name,
      this.licensePlate,
      this.keyPosition,
      this.xBaznaLokacija,
      this.xTrenutnaLokacija});

  VehicleId.fromJson(Map<String, dynamic> json) {
    name = json['name'];
    licensePlate = json['license_plate'];
    keyPosition = json['x_key_position'];
    xBaznaLokacija = json['x_bazna_lokacija'] != null
        ? new XBaznaLokacija.fromJson(json['x_bazna_lokacija'])
        : null;
    xTrenutnaLokacija = json['x_trenutna_lokacija'] != null
        ? new XTrenutnaLokacija.fromJson(json['x_trenutna_lokacija'])
        : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['name'] = this.name;
    data['license_plate'] = this.licensePlate;
    data['x_key_position'] = this.keyPosition;
    if (this.xBaznaLokacija != null) {
      data['x_bazna_lokacija'] = this.xBaznaLokacija!.toJson();
    }
    if (this.xTrenutnaLokacija != null) {
      data['x_trenutna_lokacija'] = this.xTrenutnaLokacija!.toJson();
    }
    return data;
  }
}

class XBaznaLokacija {
  double? locationLatitude;
  double? locationLongitude;

  XBaznaLokacija({this.locationLatitude, this.locationLongitude});

  XBaznaLokacija.fromJson(Map<String, dynamic> json) {
    locationLatitude = json['location_latitude'];
    locationLongitude = json['location_longitude'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['location_latitude'] = this.locationLatitude;
    data['location_longitude'] = this.locationLongitude;
    return data;
  }
}

class XTrenutnaLokacija {
  double? locationLatitude;
  double? locationLongitude;

  XTrenutnaLokacija({this.locationLatitude, this.locationLongitude});

  XTrenutnaLokacija.fromJson(Map<String, dynamic> json) {
    locationLatitude = json['location_latitude'];
    locationLongitude = json['location_longitude'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['location_latitude'] = this.locationLatitude;
    data['location_longitude'] = this.locationLongitude;
    return data;
  }
}

class RentFrom {
  String? name;

  RentFrom({this.name});

  RentFrom.fromJson(Map<String, dynamic> json) {
    name = json['name'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['name'] = this.name;
    return data;
  }
}

class CustomerId {
  String? name;
  String? phone;

  CustomerId({this.name, this.phone});

  CustomerId.fromJson(Map<String, dynamic> json) {
    name = json['name'];
    phone = json['phone'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['name'] = this.name;
    data['phone'] = this.phone;
    return data;
  }
}
