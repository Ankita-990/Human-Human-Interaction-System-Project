
# 
# Generate header file
# Path to your TFLite model file
input_file = "ann_model.tflite"
# Path to your header output file
output_file = "ann_model.cpp"

with open(input_file, "rb") as f:
    model_content = f.read()

with open(output_file, "w") as f:
    f.write("const unsigned char model[] = {\n    ")
    hex_array = []
    for idx, b in enumerate(model_content):
        # Format as C hex literal
        hex_array.append(f"0x{b:02x}")
        # Format 12 bytes per line for readability
        if (idx+1) % 12 == 0:
            hex_array.append("\n    ")
    f.write(", ".join(hex_array))
    f.write("\n};\n")
