# STL Loose Exporter

STL Loose Exporter is a Blender add-on that applys all modifiers, separates loose parts and exports them as individual STL files to be used for a 3D Printer.
It also might be used as a simple one click STL exporter.

## Features

- Separates loose parts of a selected mesh object.
- Applies all modifiers to the duplicated object before separation.
- Exports each part as an individual STL file.
- Configurable export path and scaling factor.

## Installation

1. Download the `stl_loose_exporter.py` file from the repository.
2. Open Blender.
3. Go to `Edit` > `Preferences`.
4. Select the `Add-ons` tab.
5. Click `Install` at the top.
6. Navigate to and select the `stl_loose_exporter.py` file.
7. Enable the add-on by checking the box next to it.
8. Configure path and scale factor to be used.

## Usage

1. Switch to `Object Mode` in the 3D Viewport.
2. Select the mesh object you want to process.
3. Open the sidebar by pressing `N` if it's not already open.
4. Find the `STL Loose Exporter` panel in the `Tool` tab.
5. Click the `Export Separated Parts` button.
6. The script will execute, and the exported files will be logged to the console.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Issues

If you encounter any issues, please report them on the [issue tracker](https://github.com/thhart/stl-loose-exporter/issues).

