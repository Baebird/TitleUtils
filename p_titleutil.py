import enum
import os
import shutil
import cv2
import click

# The directory of the python script
base_directory = str(os.path.dirname(os.path.abspath(__file__)))

# The directory that the cmd prompt is running in
cwdpath = str(os.getcwd())

# An enum for the modes used in szsinject
class InjectMode(enum.Enum) :
    Title = 1,
    Title_U = 2,
    Use_Here = 3


@click.group()
def cli() :
    pass

@click.command(name="GENTITLE")
@click.option("-i", type=click.STRING, required=True)
@click.option("-t", is_flag=True, default=False)
@click.option("-tu", is_flag=True, default=False)
@click.option("-uh", is_flag=True, default=False)
def GENTITLE(i, t, tu, uh):

    # Throw error if image couldn't be found
    if not ((os.path.isfile(cwdpath + "\\" + i + ".jpg")) or (os.path.isfile(cwdpath + "\\" + i + ".png"))):
        click.echo("Error: Image file supplied not found")
        exit()

    # Throw error if no template image could be found
    if (t == False) and (tu == False) and (uh == False):
        click.echo("Error: No template .szs file supplied")
        exit()

    # Attempt to load the file of the supplied name
    if os.path.isfile(cwdpath + "\\" + i + ".jpg"):
        load_image = cv2.imread(cwdpath + "\\" + i + ".jpg")
    elif os.path.isfile(cwdpath + "\\" + i + ".png") :
        load_image = cv2.imread(cwdpath + "\\" + i + ".png")

    # Make the out directory
    os.mkdir(cwdpath + "\\out")

    # Resize image and crop to make all versions of the image necessary to generate the tpls
    image = cv2.resize(load_image, (832, 456))
    cropped_image1 = image[140:456, 0:832]
    cropped_image2 = image[0:140, 0:832]

    # Write out the images as files to be passed to wimgt
    cv2.imwrite(cwdpath + "\\out\\resized.png", image)
    cv2.imwrite(cwdpath + "\\out\\resized_lower_half.png", cropped_image1)
    cv2.imwrite(cwdpath + "\\out\\resized_upper_half.png", cropped_image2)

    # Make new directory 'timg' in 'out'
    try:
        os.mkdir(cwdpath + "\\out\\timg")
    except Exception as error:
        pass

    # Generate all tpls that could be needed by whatever .szs specified
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_bokeboke.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_koopa.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_koopa_bokeboke.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_luigi.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_luigi_bokeboke.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_mario.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_mario_bokeboke.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_mario0.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_mario0_bokeboke.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_mario2.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_mario2_bokeboke.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_peachi.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_lower_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_peachi_bokeboke.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_upper_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_title_rogo_bokeboke.tpl\'')
    os.system('wimgt ENCODE \'' + cwdpath + '\\out\\resized_upper_half.png\' -x TPL -d \'' + cwdpath + '\\out\\timg\\tt_title_screen_title_rogo_r_only.tpl\'')

    # Create directory for any template files copied from the resources folder
    try:
        os.mkdir(cwdpath + "\\out\\template_title_files")
    except Exception as error:
        pass

    try:
        os.mkdir(cwdpath + "\\title")
    except Exception as error:
        pass

    # Generate a valid Title.szs file from specified image
    if t:
        shutil.copy(base_directory + "\\resources\\Title.szs", cwdpath + "\\out\\template_title_files")
        szsinject(InjectMode.Title)

    # Generate a valid Title_U.szs file from specified image
    if tu:
        shutil.copy(base_directory + "\\resources\\Title_U.szs", cwdpath + "\\out\\template_title_files")
        szsinject(InjectMode.Title_U)

    # Inject the specified image into the Title file specified
    if uh:
        szsinject(InjectMode.Use_Here)


# Add all subcommands to the CLI main command
cli.add_command(GENTITLE)

# Function for decomposing .szs file, injecting, and reassembling
def szsinject(injectionmode):
    if (injectionmode == InjectMode.Title) :
        os.system('wszst EXTRACT \'' + cwdpath + '\\out\\template_title_files\\Title.szs\' -D \'' + cwdpath + '\\out\\Title.d\'')

        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_bokeboke.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_koopa.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_koopa_bokeboke.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_luigi.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_luigi_bokeboke.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_mario.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_mario_bokeboke.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_mario0.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_mario0_bokeboke.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_mario2.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_mario2_bokeboke.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_peachi.tpl")
        os.remove(cwdpath + "\\out\\Title.d\\title\\timg\\tt_title_screen_peachi_bokeboke.tpl")

        shutil.copy(cwdpath + "\\out\\timg\\tt_title_bokeboke.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_koopa.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_koopa_bokeboke.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_luigi.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_luigi_bokeboke.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario_bokeboke.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario0.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario0_bokeboke.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario2.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario2_bokeboke.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_peachi.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_peachi_bokeboke.tpl", cwdpath + "\\out\\Title.d\\title\\timg\\")

        os.system('wszst CREATE \'' + cwdpath + '\\out\\Title.d\' -D \'' + cwdpath + '\\title\\Title.szs\'')
    elif (injectionmode == InjectMode.Title_U):
        os.system('wszst EXTRACT \'' + cwdpath + '\\out\\template_title_files\\Title_U.szs\' -D \'' + cwdpath + '\\out\\Title_U.d\'')

        os.remove(cwdpath + "\\out\\Title_U.d\\title\\timg\\tt_title_screen_mario0.tpl")
        os.remove(cwdpath + "\\out\\Title_U.d\\title\\timg\\tt_title_screen_mario0_bokeboke.tpl")
        os.remove(cwdpath + "\\out\\Title_U.d\\title\\timg\\tt_title_screen_title_rogo_bokeboke.tpl")
        os.remove(cwdpath + "\\out\\Title_U.d\\title\\timg\\tt_title_screen_title_rogo_r_only.tpl")

        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario0.tpl", cwdpath + "\\out\\Title_U.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario0_bokeboke.tpl", cwdpath + "\\out\\Title_U.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_title_rogo_bokeboke.tpl", cwdpath + "\\out\\Title_U.d\\title\\timg\\")
        shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_title_rogo_r_only.tpl", cwdpath + "\\out\\Title_U.d\\title\\timg\\")

        os.system('wszst CREATE \'' + cwdpath + '\\out\\Title_U.d\' -D \'' + cwdpath + '\\title\\Title_U.szs\'')
    elif (injectionmode == InjectMode.Use_Here):
        if os.path.isfile(cwdpath + "\\Title.szs"):
            os.system('wszst EXTRACT \'' + cwdpath + '\\Title.szs\' -D \'' + cwdpath + '\\out\\S_Title.d\'')

            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_bokeboke.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_koopa.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_koopa_bokeboke.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_luigi.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_luigi_bokeboke.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_mario.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_mario_bokeboke.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_mario0.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_mario0_bokeboke.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_mario2.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_mario2_bokeboke.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_peachi.tpl")
            os.remove(cwdpath + "\\out\\S_Title.d\\title\\timg\\tt_title_screen_peachi_bokeboke.tpl")

            shutil.copy(cwdpath + "\\out\\timg\\tt_title_bokeboke.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_koopa.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_koopa_bokeboke.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_luigi.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_luigi_bokeboke.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario_bokeboke.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario0.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario0_bokeboke.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario2.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario2_bokeboke.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_peachi.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_peachi_bokeboke.tpl", cwdpath + "\\out\\S_Title.d\\title\\timg\\")

            os.system('wszst CREATE \'' + cwdpath + '\\out\\S_Title.d\' -D \'' + cwdpath + '\\title\\S_Title.szs\'')
        elif os.path.isfile(cwdpath + "\\Title_U.szs"):
            os.system('wszst EXTRACT \'' + cwdpath + '\\Title_U.szs\' -D \'' + cwdpath + '\\out\\S_Title_U.d\'')

            os.remove(cwdpath + "\\out\\S_Title_U.d\\title\\timg\\tt_title_screen_mario0.tpl")
            os.remove(cwdpath + "\\out\\S_Title_U.d\\title\\timg\\tt_title_screen_mario0_bokeboke.tpl")
            os.remove(cwdpath + "\\out\\S_Title_U.d\\title\\timg\\tt_title_screen_title_rogo_bokeboke.tpl")
            os.remove(cwdpath + "\\out\\S_Title_U.d\\title\\timg\\tt_title_screen_title_rogo_r_only.tpl")

            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario0.tpl", cwdpath + "\\out\\S_Title_U.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_mario0_bokeboke.tpl", cwdpath + "\\out\\S_Title_U.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_title_rogo_bokeboke.tpl", cwdpath + "\\out\\S_Title_U.d\\title\\timg\\")
            shutil.copy(cwdpath + "\\out\\timg\\tt_title_screen_title_rogo_r_only.tpl", cwdpath + "\\out\\S_Title_U.d\\title\\timg\\")

            os.system('wszst CREATE \'' + cwdpath + '\\out\\S_Title_U.d\' -D \'' + cwdpath + '\\title\\S_Title_U.szs\'')


if __name__ == '__main__':
    cli()