<?php


function wp_rentals_enqueue_styles() {
	$parent_style = 'wp-rentals-style';
	wp_enqueue_style( $parent_style, get_template_directory_uri() . '/style.css' );
	wp_enqueue_style( 'wp-rentals-child-style',
        get_stylesheet_directory_uri() . '/style.css',
		array( $parent_style ),
		wp_get_theme()->get('Version')
	);
}
add_action( 'wp_enqueue_scripts', 'wp_rentals_enqueue_styles' );




add_action( 'rest_api_init', function() {
  register_rest_route( 'my/price', '/getprice', [
    'methods' => 'GET',
    'callback' => 'get_prices',
    'permission_callback' => '__return_true',
    'args'                => array(
        'current_day' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'date_from' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'date_to' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'from' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'to' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
    ),
  ] );
} );

function get_prices( $request ) {

    $current_day = $request['current_day'];
    $date_from = intval($request['date_from']);
    $date_to = intval($request['date_to']);
    $from = $request['from'];
    $to = $request['to'];
    $vehicle_category_id = $request['vehicle_category_id'];
    
    $return_array = array(
        'date_from' => $date_from,
        'date_to' => $date_to,
        'from' => $from,
        'to' => $to,
        'vehicle_category_id' => $vehicle_category_id
        );
 
 
    $duration_timestamp = $date_to - $date_from;
 
    $day_nums = ceil(($date_to - $date_from)/86400);
 
    $total_price = 0;
 
    global $wpdb;

    $price_plans = $wpdb->get_results("SELECT wp_car_rental_price_plans.price_plan_id, wp_car_rental_price_plans.start_timestamp, wp_car_rental_price_plans.end_timestamp, wp_car_rental_price_plans.daily_rate_mon, wp_car_rental_price_plans.daily_rate_tue, wp_car_rental_price_plans.daily_rate_wed, wp_car_rental_price_plans.daily_rate_thu, wp_car_rental_price_plans.daily_rate_fri, wp_car_rental_price_plans.daily_rate_sat, wp_car_rental_price_plans.daily_rate_sun, wp_car_rental_discounts.discount_percentage, wp_car_rental_discounts.discount_type, wp_car_rental_discounts.period_from, wp_car_rental_discounts.period_till FROM wp_car_rental_price_plans LEFT JOIN wp_car_rental_discounts ON wp_car_rental_price_plans.price_plan_id = wp_car_rental_discounts.price_plan_id WHERE wp_car_rental_price_plans.price_group_id = $vehicle_category_id AND ($current_day BETWEEN wp_car_rental_price_plans.start_timestamp AND wp_car_rental_price_plans.end_timestamp) AND (($duration_timestamp BETWEEN wp_car_rental_discounts.period_from AND wp_car_rental_discounts.period_till) OR wp_car_rental_discounts.period_till IS NULL)");
    // $price_plans = $wpdb->get_results("SELECT wp_car_rental_price_plans.price_plan_id, wp_car_rental_price_plans.start_timestamp,wp_car_rental_price_plans.end_timestamp,wp_car_rental_price_plans.daily_rate_mon,wp_car_rental_price_plans.daily_rate_tue,wp_car_rental_price_plans.daily_rate_wed,wp_car_rental_price_plans.daily_rate_thu,wp_car_rental_price_plans.daily_rate_fri,wp_car_rental_price_plans.daily_rate_sat,wp_car_rental_price_plans.daily_rate_sun, wp_car_rental_discounts.discount_percentage, wp_car_rental_discounts.discount_type, wp_car_rental_discounts.period_from, wp_car_rental_discounts.period_till FROM wp_car_rental_price_plans LEFT JOIN wp_car_rental_discounts ON wp_car_rental_price_plans.price_plan_id = wp_car_rental_discounts.price_plan_id WHERE wp_car_rental_price_plans.price_group_id = $vehicle_category_id AND ($date_from BETWEEN wp_car_rental_price_plans.start_timestamp)");
    // $price_plans = $wpdb->get_results("SELECT wp_car_rental_price_plans.price_plan_id, wp_car_rental_price_plans.start_timestamp,wp_car_rental_price_plans.end_timestamp,wp_car_rental_price_plans.daily_rate_mon,wp_car_rental_price_plans.daily_rate_tue,wp_car_rental_price_plans.daily_rate_wed,wp_car_rental_price_plans.daily_rate_thu,wp_car_rental_price_plans.daily_rate_fri,wp_car_rental_price_plans.daily_rate_sat,wp_car_rental_price_plans.daily_rate_sun, wp_car_rental_discounts.discount_percentage, wp_car_rental_discounts.discount_type, wp_car_rental_discounts.period_from, wp_car_rental_discounts.period_till FROM wp_car_rental_price_plans LEFT JOIN wp_car_rental_discounts ON wp_car_rental_price_plans.price_plan_id = wp_car_rental_discounts.price_plan_id WHERE wp_car_rental_price_plans.price_group_id = $vehicle_category_id AND (($date_from BETWEEN wp_car_rental_price_plans.start_timestamp AND wp_car_rental_price_plans.end_timestamp) OR ($date_to BETWEEN wp_car_rental_price_plans.start_timestamp AND wp_car_rental_price_plans.end_timestamp)) AND ($duration_timestamp BETWEEN wp_car_rental_discounts.period_from AND wp_car_rental_discounts.period_till OR wp_car_rental_discounts.period_till IS NULL)");
 
    return $price_plans;
}



add_action( 'rest_api_init', function() {
  register_rest_route( 'my/price', '/getpriceextras', [
    'methods' => 'GET',
    'callback' => 'get_prices_extras',
    'permission_callback' => '__return_true',
    'args'                => array(
        'date_from' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'date_to' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'from' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'to' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
    ),
  ] );
} );

function get_prices_extras( $request ) {

    $date_from = intval($request['date_from']);
    $date_to = intval($request['date_to']);
    $from = $request['from'];
    $to = $request['to'];
    $vehicle_category_id = $request['vehicle_category_id'];
    
    $return_array = array(
        'date_from' => $date_from,
        'date_to' => $date_to,
        'from' => $from,
        'to' => $to,
        'vehicle_category_id' => $vehicle_category_id
        );
 
 
    $duration_timestamp = $date_to - $date_from;
 
    $day_nums = ceil(($date_to - $date_from)/86400);
 
    $total_price = 0;
 
    global $wpdb;

    $price_plans = $wpdb->get_results("SELECT wp_car_rental_extras.price, wp_car_rental_discounts.discount_percentage, wp_car_rental_extras.extra_id, wp_car_rental_discounts.period_from, wp_car_rental_discounts.period_till FROM wp_car_rental_extras LEFT JOIN wp_car_rental_discounts ON wp_car_rental_discounts.extra_id = wp_car_rental_extras.extra_id WHERE wp_car_rental_extras.item_id = $vehicle_category_id  AND ($duration_timestamp BETWEEN wp_car_rental_discounts.period_from AND wp_car_rental_discounts.period_till OR wp_car_rental_discounts.period_till IS NULL) AND wp_car_rental_extras.extra_name LIKE 'SCDW%'");
 
    return $price_plans;
}



add_action( 'rest_api_init', function() {
  register_rest_route( 'my/price', '/cardeposit', [
    'methods' => 'GET',
    'callback' => 'car_deposit',
    'permission_callback' => '__return_true',
    'args'                => array(
        'car_id' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
    ),
  ] );
} );

function car_deposit( $request ) {

    $car_id = intval($request['car_id']);


 
    global $wpdb;

    $deposit = $wpdb->get_results("SELECT wp_car_rental_items.fixed_rental_deposit, wp_car_rental_extras.price FROM wp_car_rental_items LEFT JOIN wp_car_rental_extras ON wp_car_rental_extras.item_id = wp_car_rental_items.item_id WHERE wp_car_rental_items.item_id = $car_id AND wp_car_rental_extras.extra_name LIKE 'SCDW%'");
 
    return $deposit;
}

add_action( 'rest_api_init', function() {
  register_rest_route( 'my/price', '/extras', [
    'methods' => 'GET',
    'callback' => 'car_extras',
    'permission_callback' => '__return_true',
  ] );
} );

function car_extras( $request ) {

    $car_id = intval($request['car_id']);


 
    global $wpdb;

    $extras = $wpdb->get_results("SELECT extra_id, extra_name, price FROM wp_car_rental_extras");
 
    return $extras;
}



// GET INSURANCE

add_action( 'rest_api_init', function() {
  register_rest_route( 'my/price', '/getpriceinsurance', [
    'methods' => 'GET',
    'callback' => 'get_prices_insurance',
    'permission_callback' => '__return_true',
    'args'                => array(
        'date_from' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'date_to' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
    ),
  ] );
} );

function get_prices_insurance( $request ) {

    $date_from = intval($request['date_from']);
    $date_to = intval($request['date_to']);
    $vehicle_id = $request['vehicle_id'];


 

    $duration_timestamp = $date_to - $date_from;
 

    global $wpdb;

    $price_plans = $wpdb->get_results("SELECT wp_car_rental_extras.price, wp_car_rental_discounts.discount_percentage, wp_car_rental_extras.extra_id, wp_car_rental_discounts.period_from, wp_car_rental_discounts.period_till FROM wp_car_rental_extras LEFT JOIN wp_car_rental_discounts ON wp_car_rental_discounts.extra_id = wp_car_rental_extras.extra_id WHERE wp_car_rental_extras.item_id = $vehicle_id  AND ($duration_timestamp BETWEEN wp_car_rental_discounts.period_from AND wp_car_rental_discounts.period_till OR wp_car_rental_discounts.period_till IS NULL) AND wp_car_rental_extras.extra_name LIKE 'SCDW%'");
 
    return $price_plans;
}



// GET PRICE TYRES


add_action( 'rest_api_init', function() {
  register_rest_route( 'my/price', '/getpriceextrastyres', [
    'methods' => 'GET',
    'callback' => 'get_prices_extras_tyres',
    'permission_callback' => '__return_true',
    'args'                => array(
        'date_from' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'date_to' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'from' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'to' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
    ),
  ] );
} );

function get_prices_extras_tyres( $request ) {

    $date_from = intval($request['date_from']);
    $date_to = intval($request['date_to']);
    $from = $request['from'];
    $to = $request['to'];
    $vehicle_category_id = $request['vehicle_category_id'];
    
    $return_array = array(
        'date_from' => $date_from,
        'date_to' => $date_to,
        'from' => $from,
        'to' => $to,
        'vehicle_category_id' => $vehicle_category_id
        );
 
 
    $duration_timestamp = $date_to - $date_from;
 
    $day_nums = ceil(($date_to - $date_from)/86400);
 
    $total_price = 0;
 
    global $wpdb;

    $price_plans = $wpdb->get_results("SELECT wp_car_rental_extras.extra_id, wp_car_rental_extras.extra_name, wp_car_rental_extras.price, wp_car_rental_discounts.discount_percentage FROM wp_car_rental_extras LEFT JOIN wp_car_rental_discounts ON wp_car_rental_discounts.extra_id = wp_car_rental_extras.extra_id WHERE wp_car_rental_extras.extra_name = 'TP-Tyres Protection. Required without credit card. Price per rental:'  AND ($duration_timestamp BETWEEN wp_car_rental_discounts.period_from AND wp_car_rental_discounts.period_till OR wp_car_rental_discounts.period_till IS NULL)");
 
    return $price_plans;
}

// GET PRICE TYRES FROM ID


add_action( 'rest_api_init', function() {
  register_rest_route( 'my/price', '/getpriceextrastyresfromid', [
    'methods' => 'GET',
    'callback' => 'get_prices_extras_tyres_from_id',
    'permission_callback' => '__return_true',
    'args'                => array(
        'date_from' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'date_to' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'from' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'to' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
    ),
  ] );
} );

function get_prices_extras_tyres_from_id( $request ) {

    $date_from = intval($request['date_from']);
    $date_to = intval($request['date_to']);

 
    $duration_timestamp = $date_to - $date_from;
 
    global $wpdb;

    $price_plans = $wpdb->get_results("SELECT wp_car_rental_extras.extra_id, wp_car_rental_extras.extra_name, wp_car_rental_extras.price, wp_car_rental_discounts.discount_percentage FROM wp_car_rental_extras LEFT JOIN wp_car_rental_discounts ON wp_car_rental_discounts.extra_id = wp_car_rental_extras.extra_id WHERE wp_car_rental_extras.extra_name = 'TP-Tyres Protection. Required without credit card. Price per rental:'  AND ($duration_timestamp BETWEEN wp_car_rental_discounts.period_from AND wp_car_rental_discounts.period_till OR wp_car_rental_discounts.period_till IS NULL)");
 
    return $price_plans;
}






// GET PRICE SNOWCHAIN FROM ID


add_action( 'rest_api_init', function() {
  register_rest_route( 'my/price', '/getpricesnowchain', [
    'methods' => 'GET',
    'callback' => 'get_prices_snowchain',
    'permission_callback' => '__return_true',
  ] );
} );

function get_prices_snowchain( $request ) {

    // $date_from = intval($request['date_from']);
    // $date_to = intval($request['date_to']);

 
    // $duration_timestamp = $date_to - $date_from;
 
    global $wpdb;

    $price_plans = $wpdb->get_results("SELECT wp_car_rental_extras.extra_id, wp_car_rental_extras.extra_name, wp_car_rental_extras.price FROM wp_car_rental_extras WHERE extra_name LIKE 'Snow Chains%'");
 
    return $price_plans;
}



// update database



add_action( 'rest_api_init', function() {
  register_rest_route( 'my/price', '/updatedata', [
    'methods' => 'POST',
    'callback' => 'update_database',
    'permission_callback' => '__return_true',
    'args'                => array(
        'item_id' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
        'enabled' => array(
            'validate_callback' => function( $param, $request, $key ) {
                return $param;
            }
        ),
    ),

  ] );
} );



function update_database($request) {
    
    
    $item_id = intval($request['item_id']);
    $enabled = intval($request['enabled']);
    
    global $wpdb;
    

    $data = array(
        'enabled' => $enabled
    );
    $data_where = array(
        'item_id' => $item_id
    );
    $wpdb->update('wp_car_rental_items' , $data, $data_where);
}































?>