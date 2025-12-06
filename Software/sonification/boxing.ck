//Author: Santiago Hernandez & Gabe Rottet

// Define an array of string to hold your file paths
/*
string samples[];
*/

me.dir() + "../data_reading/named_pipe.fifo" => string named_pipe_path;
// Add your .wav file paths to the array
// Make sure to use forward slashes in the path, even on Windows
FileIO sound_dir;
me.dir() + "sound_files/" => string sound_file_path;
sound_dir.open(sound_file_path, FileIO.READ);
sound_dir.dirList() @=> string sound_files[];
string samples[sound_files.size()];
for (int i; i < sound_files.size(); i++){
    sound_file_path + sound_files[i] => samples[i];
}

sound_dir.close();

FileIO named_pipe;
named_pipe.open(named_pipe_path, FileIO.READ);

string line;
StringTokenizer tokenizer;
tokenizer.delims(", ");

int token_index;
float accel[6];
float piezo;
int timestamp;
// Seed the random number generator (optional, but good practice)
// Using now::ms as a seed ensures a different sequence each run
//now::ms() => Std.srandom;
1 => Math.srandom;

// Create a SndBuf object to load and play the audio
SndBuf buffer => Bitcrusher crush => JCRev rev => dac;
0.8 => buffer.gain;
0.7 => rev.gain;
0.7 => crush.gain;

// Loop indefinitely to play random files
fun playRandomFile() {
   
    named_pipe.readLine() => line;
    <<< line >>>;
    
    if (line == null) {
        <<< "pipe other end is closed" >>>;
        me.exit();
    }

    tokenizer.set(line);
    Std.atof(tokenizer.get(0)) => accel[0];
    Std.atof(tokenizer.get(1)) => accel[1];
    Std.atof(tokenizer.get(2)) => accel[2];
    Std.atof(tokenizer.get(3)) => accel[3];
    Std.atof(tokenizer.get(4)) => accel[4];
    Std.atof(tokenizer.get(5)) => accel[5];
    Std.atof(tokenizer.get(6)) => piezo;
    Std.atoi(tokenizer.get(7)) => timestamp;
    
    <<< piezo >>>;
    <<< timestamp >>>;
    
    /*
           
    // Generate a random index between 0 and the last index of the array
    // Math.random2(min, max) generates an integer in the range [min, max]
    Math.random2(0, samples.size() - 1) => int randomIndex;

    // Get the random file path from the array
    samples[randomIndex] => string randomFile;

    // Load the randomly selected file into the buffer
    randomFile => buffer.read;

    // Play the file
    // Set position to the end of the buffer (buffer.samples() is total samples)
    buffer.samples() => buffer.pos;
    // Set position to 0 to start playback from the beginning
    0 => buffer.pos;
    
    // Wait for the duration of the sample before the next iteration
    // The "now" keyword advances time by the buffer length
    buffer.length() => now;
    */
    1::ms => now;
}

while (true) {
    playRandomFile();
}

/*

//with reverb

// ... (file array and random selection code goes here) ...

// Create the audio buffer unit generator
SndBuf buffer;

// Create an effects unit generator (e.g., a simple reverb)
JCRev reverb => dac;

// Patch the buffer THROUGH the reverb unit, then to the DAC
buffer => reverb => dac;

// Load and read the selected WAV file into the buffer
"path/to/your/file1.wav" => buffer.read; // Use your actual file path variable here

// Configure the effect parameters (e.g., set the reverb mix/room size)
0.5 => reverb.mix; // Mix between wet and dry signal (0.0 to 1.0)

// Play the entire length of the audio file and wait until it finishes
buffer.length() => now; 
// Note: JCRev automatically adds a decay time after the buffer finishes playing.
// The script will wait until the reverb tail naturally fades out.

//Use code with caution.

*/

/*

//with distortion 

​// Define an array of strings containing the paths to your WAV files
string wavFiles[] = {
    "path/to/your/file1.wav",
    "path/to/your/file2.wav",
    "path/to/your/file3.wav",
    "path/to/your/file4.wav"
};

// Seed the random number generator
now / 1::samp => int seed;
Math.srandom(seed);

// Create the audio buffer unit generator
SndBuf buffer;

// Create the distortion effect unit generator
Bitcrusher crush;

// Patch the signal flow: buffer -> distortion -> dac
buffer => crush => dac;

// Generate a random integer between 0 and the number of files minus 1
Math.random2(0, wavFiles.size() - 1) => int randomIndex;

// Get the random file path from the array
wavFiles[randomIndex] => string fileToPlay;

// Load and read the selected WAV file into the buffer
fileToPlay => buffer.read;

// --- Configure the distortion parameters ---
// Lower bits mean harsher quantization noise (more distortion)
8 => crush.bits; // Reduce sample width to 8 bits (default is 32)

// Higher downsample factor means lower sample rate (more aliasing/distortion)
4 => crush.downsampleFactor; // Downsample by a factor of 4

// You might need to adjust the gain to avoid digital clipping, as distortion increases volume
// All UGens have a .gain() function
0.8 => buffer.gain;
0.7 => crush.gain;

// Play the entire length of the audio file and wait until it finishes
buffer.length() => now;

*/

// The script ends here
