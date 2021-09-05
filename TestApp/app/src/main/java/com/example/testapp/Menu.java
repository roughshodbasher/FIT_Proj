package com.example.testapp;

public class Menu {

    private String name;

    public Menu(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Menu{" +
                "name='" + name + '\'' +
                '}';
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
