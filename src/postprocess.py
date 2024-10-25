from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import json

def add_text_to_image(input_image_path, output_image_path, added_height, text_lines, font_size=14, stroke_width=3):
    # Load the image
    image = Image.open(input_image_path)

    # Add white space to the height of the image
    new_height = image.height + added_height
    new_image = Image.new("RGB", (image.width, new_height), "white")
    new_image.paste(image, (0, 0))

    # Draw text on the added white space
    draw = ImageDraw.Draw(new_image)

    # Specify the font and size
    # font = ImageFont.truetype("arial.ttf", size=font_size)
    font = ImageFont.truetype("fonts/dejavu.ttf", size=font_size)

    # Set the starting position for the text
    text_position = (100, image.height + 10)

    # Write each line of text
    for line in text_lines:
        # Calculate text size using bounding box
        text_bbox = draw.textbbox(text_position, line, font=font, stroke_width=stroke_width)
        text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

        # Draw text on the image
        draw.text(text_position, line, fill="black", font=font)

        # Update text position for the next line
        text_position = (text_position[0], text_position[1] + text_size[1] + 5)  # Adjust the spacing

    # Save the final image
    new_image.save(output_image_path)

def read_csv_from_json(in_filename):
    # Read the dictionary from the JSON file
    with open(in_filename, 'r') as json_file:
        loaded_data = json.load(json_file)

    csv_string =  f'tau: {loaded_data["tau"]},'
    csv_string += f'delta: {loaded_data["delta"]},'
    csv_string += f'mu: {loaded_data["mu"]},'
    csv_string += f'porosity: {loaded_data["porosity"]},'
    csv_string += f'correction: {loaded_data["effective_porosity"]},'
    csv_string += f'max_iters: {loaded_data["maxiters"]},'
    csv_string += f'dir: {loaded_data["output_dir"]},'
    csv_string += f'flow_solver: {loaded_data["flow_solver"]},'
    csv_string += f'Re: {loaded_data["Re"]},'
    csv_string += f'Da: {loaded_data["Da"]},'
    csv_string += f'u_in: {loaded_data["u_in"]},'
    csv_string += f'full_NS: {not loaded_data["solve_stokes"]},'
    csv_string += f'charge: {not loaded_data["no_charge"]},'
    csv_string += f'flow: {not loaded_data["no_flow"]},'
    csv_string += f'elec_contrib: {loaded_data["elec_contrib_ratio"]}'

    return csv_string


def convert_csv_to_multiple_lines(csv_string, rows_per_line):
    # Split the CSV string into individual elements
    csv_data = csv_string.split(',')

    # Split the elements into chunks based on the specified number of rows per line
    row_chunks = [csv_data[i:i + rows_per_line] for i in range(0, len(csv_data), rows_per_line)]

    # Calculate the maximum width for each column
    column_widths = [max(len(element) for element in column) for column in zip(*row_chunks)]

    output_list = []
    for chunk in row_chunks:
        aligned_row = (' '*7).join(element.ljust(width) for element, width in zip(chunk, column_widths))
        output_list.append(aligned_row)
        print(aligned_row)

    return output_list

if __name__ == "__main__":

    # Set up argument parser
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input_dir", type=str, default="./results")
    parser.add_argument("--out_name", type=str, default="./out")
    parser.add_argument("--loss_plot_only", action="store_true", default=False)

    args, _ = parser.parse_known_args()
    input_dir = args.input_dir
    out_raw_filename = args.out_name + "-raw.png"
    out_filename = args.out_name + ".png"
    loss_out_filename = args.out_name + "-loss.png"
    loss_in_filename = input_dir + "/data/losses.txt"
    args_in_filename = input_dir + "/data/args.json"

    loss_plot_only = args.loss_plot_only

    if not loss_plot_only:
        csv_string = read_csv_from_json(args_in_filename)
        # csv_string = "tau: 0.005,delta: 1,mu: 0.1,posority: 0.5,correction: effective,maxiters: 80,dir: ./results-1,flow_solver: direct,Re: 1.0,Da: 1e-4,u_in: 1.0,full_NS: yes,charge: yes,flow: yes, elec_contrib: 1.0"

        # Generate isocontour plots using ParaView
        cmd = f"pvpython make_screenshot.py --input_dir {input_dir} --out_name {out_raw_filename}"
        os.system(cmd)

        input_path = out_raw_filename # Should be created by ParaView by now
        rows_per_line = 3
        font_size = 46
        added_height = 300

        text_lines = convert_csv_to_multiple_lines(csv_string, rows_per_line)
        # print(text_lines)

        add_text_to_image(input_path, out_filename, added_height, text_lines, font_size)

    # Generate loss plot
    cmd = f"python plot_loss.py --input_file {loss_in_filename} --out_name {loss_out_filename}"
    os.system(cmd)
