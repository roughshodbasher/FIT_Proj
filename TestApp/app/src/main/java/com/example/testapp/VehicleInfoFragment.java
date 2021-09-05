package com.example.testapp;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import com.example.testapp.databinding.FragmentVehicleInfoBinding;

public class VehicleInfoFragment extends Fragment {

    private FragmentVehicleInfoBinding binding;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentVehicleInfoBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        binding.newVehicleButton.setOnClickListener(this::onClick);

    }

    private void onClick(View view) {
        switch (view.getId()) {
            case R.id.newVehicleButton:
                NavHostFragment.findNavController(VehicleInfoFragment.this)
                        .navigate(R.id.action_VehicleInfoFragment_to_NewVehicleInfoFragment);
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

}