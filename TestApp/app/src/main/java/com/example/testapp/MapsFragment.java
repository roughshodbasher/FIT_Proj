package com.example.testapp;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;

import android.app.ActivityManager;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import com.example.testapp.databinding.FragmentMapsBinding;
import com.example.testapp.databinding.FragmentStartTripBinding;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Polyline;
import com.google.android.gms.maps.model.PolylineOptions;
import com.google.maps.internal.PolylineEncoding;

import java.util.ArrayList;
import java.util.List;

import static android.content.ContentValues.TAG;
import static android.content.Context.ACTIVITY_SERVICE;
import static androidx.core.content.ContextCompat.getSystemService;

public class MapsFragment extends Fragment {

    private GoogleMap mGoogleMap;
    private static MapsFragment instance = null;
    private String polyLine = "knkmEh|vnUuAuCq@q@eBe@{Cg@eBCuEb@_GvA{Ar@gG`BiEz@oBbAgH~FsBnByCfBgOpOuDvDsBrCkHhKm@`@s@Hy@?AhBi@rG]rITlO?nIBly@Enr@@~A{CBqOJsD@gDRcE@a@?{AQaHF_JAmEe@gDCkET{HZuDH{DBaBQ}OB{BR{EBoC?qBBwBLkF?}KFs@??|@?v@@lFBbOBlV@vBc@?gABqABiRD_H@?mBjB?zIA?jB`MCpACfACb@??jA?z@@lAAfIBrM@jLD~\\@lCBnB[pAKb@[dBHjDDrEe@rEOr@@~@}@hC_DjHeFlJ{IjP}Uvi@yJjTuIxRaDpGu@hAeFvGkFjH_CvDoBpDu@~@w@?mAzBeEbKcA`DwEdNuDlJ_IrQgBdE}DjJiDnGuDdHsCvG}AzDwDvHeEtJyUvk@wBrFaK|TkG`MwM`XqNp[uFxL}DhHsG|JoDpE}JfKmTrTeBvByCrEiDxGoE|JyDrGiEjG_DrD{FlFqQnLs_@xUu[vRgO`KoBfAmKlH}ExCuB|@eIdD_Ch@iRdEgBPmAIwBm@MEa@HaCiAgGiC}E{B}NoHiLsFy_@kRcFyByJyCsSoGoWiI_I}CsOaHm@g@iCgAeFmBqHqBaFyAi@]]cA@YJo@nIxBHT|Bj@^LW`Bs@vCK\\}@vAc@Xy@Ic@q@@eA^k@r@K~Dz@vGlBxIpDtIlDpCjAj@CjFjBbGnBrEtAzQtFbQnFhHlCj\\hPrd@bUta@|Pn`@lP`T|ItD`BvJnDbPvDhKzA|Jx@rUf@jb@n@d_@f@|\\d@lHKr]w@l}@kBtBCbTm@vLy@lHmAlSuEfW}Gfh@yM~XsHzG{AxJyAbIkAzR{C~O_CdKkBfDiAtJgE~JwE|GkDlW{Ll\\}OnSkJrKeDtMsCxHcApJs@nQWbR@lT@~R?vLBpNI`C@fF^dDr@jGjCfDbCbDfDhBpBtDbDnC`BtF~Bf[bInLzCxRpHfI`D~EfAvG`@~BIjEg@~Aa@zDcBxMqHxAgAt@cApCsDjCwF|AkG^_I?qd@FaoAJ}eA?w]H_E?mIJwHOqG[iDw@sIC{ELmD`@_HP_b@@y`@D_e@Fw[@cGUuHBeBG{FByFr@aAPGr@@?{D?_EAqJEiJG_EAiGCoB?]h@?vA?wA?i@??eB?yAA}AAeJA_N@uMeUFqVHksAZ}\\Pmg@F}YJAgHIma@WakAQe_AMab@Gck@Cys@AgbAAmNEaEsK@?uN@cHA_@W?mD@s@AiBk@_BiBGM";

    private OnMapReadyCallback callback = new OnMapReadyCallback() {

        /**
         * Manipulates the map once available.
         * This callback is triggered when the map is ready to be used.
         * This is where we can add markers or lines, add listeners or move the camera.
         * In this case, we just add a marker near Sydney, Australia.
         * If Google Play services is not installed on the device, the user will be prompted to
         * install it inside the SupportMapFragment. This method will only be triggered once the
         * user has installed Google Play services and returned to the app.
         */
        @Override
        public void onMapReady(GoogleMap googleMap) {
            mGoogleMap = googleMap;
            if (polyLine != "") {
                Toast.makeText(getContext(), "should display route", Toast.LENGTH_SHORT).show();
                addPolylinesToMap(polyLine);
            } else {
                Toast.makeText(getContext(), "map ready", Toast.LENGTH_SHORT).show();
                googleMap.getUiSettings().setZoomControlsEnabled(true);
                LatLng monash = new LatLng(-37.9144, 145.1300);
                googleMap.addMarker(new MarkerOptions().position(monash).title("Monash University"));
                googleMap.moveCamera(CameraUpdateFactory.newLatLng(monash));
                googleMap.moveCamera(CameraUpdateFactory.zoomTo(15));
            }
        }
    };

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_maps, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        SupportMapFragment mapFragment =
                (SupportMapFragment) getChildFragmentManager().findFragmentById(R.id.map);
        if (mapFragment != null) {
            mapFragment.getMapAsync(callback);
        }
        instance = this;
    }

    public void addPolylinesToMap(final String polyLine){
        new Handler(Looper.getMainLooper()).post(new Runnable() {
            @Override
            public void run() {
                    List<com.google.maps.model.LatLng> decodedPath = PolylineEncoding.decode(polyLine);
                    List<LatLng> newDecodedPath = new ArrayList<>();
                    for(com.google.maps.model.LatLng latLng: decodedPath){
                        newDecodedPath.add(new LatLng(
                                latLng.lat,
                                latLng.lng
                        ));
                        Log.d(TAG, latLng.lat + "-" + latLng.lng);;
                    Polyline polyline = mGoogleMap.addPolyline(new PolylineOptions().addAll(newDecodedPath));
                    polyline.setColor(ContextCompat.getColor(getActivity(), R.color.quantum_googblue));
                    polyline.setClickable(true);
                    zoomRoute(newDecodedPath);
                }
            }
        });
    }

    public void zoomRoute(List<LatLng> lstLatLngRoute) {

        if (mGoogleMap == null || lstLatLngRoute == null || lstLatLngRoute.isEmpty()) return;

        LatLngBounds.Builder boundsBuilder = new LatLngBounds.Builder();
        for (LatLng latLngPoint : lstLatLngRoute)
            boundsBuilder.include(latLngPoint);

        int routePadding = 120;
        LatLngBounds latLngBounds = boundsBuilder.build();

        mGoogleMap.animateCamera(
                CameraUpdateFactory.newLatLngBounds(latLngBounds, routePadding),
                600,
                null
        );
    }

    public static MapsFragment getInstance() {
        return instance;
    }

    public void readyRoute(String poly) {
        polyLine = poly;
    }

}