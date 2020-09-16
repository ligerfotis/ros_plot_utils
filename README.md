# ros_plot_utils

### Strip csv files
To strip csv files exported from the rosbag ones using [rosbag_pandas](https://github.com/eurogroep/rosbag_pandas) place them in the `data` directory and then run:
    
        python strip_csv.py <live or on_demand>

The striped csv files for all files in `data` dir will be in the `stripped_final` directory

### Plot aperture
After obtaining the stripped files, the aperture between index and thumb tips can be plotted for all the files in the `stripped_final` directory 

        python plot_aperture.py <live or on_demand> <aperture or keypoints>
        
(\* keypoints option is not tested)
        
        
##### Notice: There is a requirements.txt file containing all packages needed to run the above code.

