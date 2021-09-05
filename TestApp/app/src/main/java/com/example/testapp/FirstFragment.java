package com.example.testapp;

import android.content.res.Resources;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;
import androidx.recyclerview.widget.RecyclerView;

import com.example.testapp.databinding.FragmentFirstBinding;
import com.google.android.material.card.MaterialCardView;

public class FirstFragment extends Fragment {

    private FragmentFirstBinding binding;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentFirstBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        binding.startCardView.setOnClickListener(this::onClick);
        binding.mapCardView.setOnClickListener(this::onClick);
        binding.analyticsCardView.setOnClickListener(this::onClick);
        binding.vehicleCardView.setOnClickListener(this::onClick);
    }

    private void onClick(View view) {
        switch (view.getId()) {
            case R.id.startCardView:
                //Toast.makeText(getContext(), "Start Card Clicked", Toast.LENGTH_SHORT).show();
                NavHostFragment.findNavController(FirstFragment.this)
                        .navigate(R.id.action_FirstFragment_to_StartTripFragment);
                break;
            case R.id.mapCardView:
                //Toast.makeText(getContext(), "Map Card Clicked", Toast.LENGTH_SHORT).show();
                NavHostFragment.findNavController(FirstFragment.this)
                        .navigate(R.id.action_FirstFragment_to_MapsFragment);
                break;
            case R.id.analyticsCardView:
                //Toast.makeText(getContext(), "Analytics Card Clicked", Toast.LENGTH_SHORT).show();
                NavHostFragment.findNavController(FirstFragment.this)
                        .navigate(R.id.action_FirstFragment_to_AnalyticsFragment);
                break;
            case R.id.vehicleCardView:
                //Toast.makeText(getContext(), "Vehicle Card Clicked", Toast.LENGTH_SHORT).show();
                NavHostFragment.findNavController(FirstFragment.this)
                        .navigate(R.id.action_FirstFragment_to_VehicleInfoFragment);

                break;
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }


}