package com.example.testapp;

import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class MenuRecViewAdapter extends RecyclerView.Adapter<MenuRecViewAdapter.ViewHolder>{

    private ArrayList<Menu> menuItemAL = new ArrayList<>();

    public MenuRecViewAdapter() {

    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        return null;
    }

    public void setMenuItemAL(ArrayList<Menu> menuItemAL) {
        this.menuItemAL = menuItemAL;
    }

    @Override
    public void onBindViewHolder(@NonNull MenuRecViewAdapter.ViewHolder holder, int position) {

    }

    @Override
    public int getItemCount() {
        return 0;
    }

    public class ViewHolder extends RecyclerView.ViewHolder{

        private TextView txtName;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            txtName = itemView.findViewById(R.id.MenuText);
        }
    }

}
