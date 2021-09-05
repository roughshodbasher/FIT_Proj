package com.example.testapp;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

import com.example.testapp.databinding.FragmentStartTripBinding;
import com.google.android.gms.common.api.Status;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.libraries.places.api.Places;
import com.google.android.libraries.places.api.model.Place;
import com.google.android.libraries.places.api.model.RectangularBounds;
import com.google.android.libraries.places.api.model.TypeFilter;
import com.google.android.libraries.places.widget.Autocomplete;
import com.google.android.libraries.places.widget.AutocompleteActivity;
import com.google.android.libraries.places.widget.model.AutocompleteActivityMode;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

import static android.content.Context.LOCATION_SERVICE;

public class StartTripFragment extends Fragment {

    private FragmentStartTripBinding binding;
    private String[] carVIN = {"ABC123", "DEF456", "JKL789", "HIJ012", "LMN345"};
    private List<String> destinationListStr = new ArrayList<String>();
    private ArrayAdapter<String> destinationListAdapter;
    private EditText autocompleteEditText;
    private Intent autocompleteIntent;
    private LocationManager locationManager;
    private String currentAddress;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentStartTripBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        //destination list adapter
        destinationListAdapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_1, destinationListStr);
        binding.destinationsList.setAdapter(destinationListAdapter);

        //car VIN autocomplete
        ArrayAdapter<String> adapter = new ArrayAdapter<>(getContext(),android.R.layout.select_dialog_item,carVIN);
        AutoCompleteTextView autoCompleteTextView = binding.carAutoCompleteText;
        autoCompleteTextView.setThreshold(1);
        autoCompleteTextView.setAdapter(adapter);

        // places intent builder
        List<Place.Field> fieldList = Arrays.asList(Place.Field.ADDRESS, Place.Field.LAT_LNG, Place.Field.NAME);
        autocompleteIntent = new Autocomplete.IntentBuilder(AutocompleteActivityMode.OVERLAY, fieldList)
                .setLocationBias(RectangularBounds.newInstance(
                        //SW Corner
                        new LatLng(-39, 143.5),
                        //NE Corner
                        new LatLng(-37, 146)
                ))
                .setCountry("AU")
                .build(getContext());

        //places autocomplete
        binding.fromEditText.setFocusable(false);
        binding.destinationsEditText.setFocusable(false);
        Places.initialize(getContext(), "AIzaSyANO9QSl-t37uZDHAvJyFONA7Mty3TL9Y0");
        binding.fromEditText.setOnClickListener(this::onClickAuto);
        binding.destinationsEditText.setOnClickListener(this::onClickAuto);

        //location manager
        if (ContextCompat.checkSelfPermission(getContext(), Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(getActivity(), new String[]{
                    Manifest.permission.ACCESS_FINE_LOCATION
            }, 100);
        }

        binding.currentLocationButton.setOnClickListener(this::onClick);
        binding.addDestinationButton.setOnClickListener(this::onClick);

    }

    public void onClickAuto(View view){
        startActivityForResult(autocompleteIntent, 100);
        switch (view.getId()) {
            case R.id.fromEditText:
                autocompleteEditText = binding.fromEditText;
                break;
            case R.id.destinationsEditText:
                autocompleteEditText = binding.destinationsEditText;
                break;
        }
    }

    public void onClick(View view){
        switch (view.getId()) {
            case R.id.addDestinationButton:
                destinationListStr.add(binding.destinationsEditText.getText().toString());
                binding.destinationsEditText.setText("");
                destinationListAdapter.notifyDataSetChanged();
                break;
            case R.id.currentLocationButton:
                /*
                Toast.makeText(getContext(), "location button pressed", Toast.LENGTH_SHORT).show();
                if (!isConnected(this)) {
                    Toast.makeText(getContext(), "no internet", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(getContext(), "internet connected", Toast.LENGTH_SHORT).show();
                }
                ((MainActivity)getActivity()).getLocation();
                currentAddress = ((MainActivity)getActivity()).getCurrentAddress();
                binding.fromEditText.setText(currentAddress);*/
                binding.fromEditText.setText("Wellington Rd, Clayton VIC 3800, Australia");
                break;
        }
    }

    private boolean isConnected(StartTripFragment startTripFragment) {
        ConnectivityManager connectivityManager = (ConnectivityManager) getContext().getSystemService(Context.CONNECTIVITY_SERVICE);

        NetworkInfo wifiConn = connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI);
        NetworkInfo mobileConn = connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_MOBILE);

        if ((wifiConn!=null && wifiConn.isConnected()) || (mobileConn!=null && mobileConn.isConnected())) {
            return true;
        } else {
            return false;
        }

    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 100 && resultCode == -1) {
            Place place = Autocomplete.getPlaceFromIntent(data);
            autocompleteEditText.setText(place.getAddress());
        } else if (resultCode == AutocompleteActivity.RESULT_ERROR) {
            Status status = Autocomplete.getStatusFromIntent(data);
            Toast.makeText(getContext(), status.getStatusMessage(), Toast.LENGTH_SHORT).show();
        }

    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }


}