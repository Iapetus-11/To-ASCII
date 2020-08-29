
def main():
    import argparse

    from .Image import Image
    from .Video import Video
    from .Live import Live

    parser = argparse.ArgumentParser(
        prog='to-ascii',
        description='A tool which can convert videos, images, gifs, and even live video to ascii art!'
    )

    # cli args
    parser.add_argument('-t', '--type', type=str, choices=['image', 'video', 'live'], dest='filetype', help='The type of file', action='store', required=True)
    parser.add_argument('-f', '--file', type=str, dest='filename', help='The name of the file to convert', action='store', required=True)
    parser.add_argument('-s', '--scale', type=float, dest='scale', default=.1, help='The scale of the final dimensions', action='store')
    parser.add_argument('-w', '--width-stretch', type=float, dest='width_stretch', default=2, help='Scale which only applies to the width', action='store')
    parser.add_argument('-g', '--gradient', type=str, dest='gradient', default='0', help='The gradient pattern which will be used', action='store')

    args = parser.parse_args()

    try:  # attempt to make gradient an integer if the gradient was supposed to be an index
        args.gradient = int(args.gradient)
    except ValueError:
        pass

    if args.filetype == 'live':
        try:
            source = int(args.filename)
        except ValueError:
            source = 0

        l = Live(source, scale=args.scale, w_stretch=args.width_stretch, gradient=args.gradient, fps=25, verbose=True)

        try:
            l.view()
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(f'ERROR (Please report this!): {e}')
            return

    elif args.filetype == 'video':
        c = Video(args.filename, scale=args.scale, w_stretch=args.width_stretch, gradient=args.gradient, verbose=True)
    else:
        c = Image(args.filename, scale=args.scale, w_stretch=args.width_stretch, gradient=args.gradient, verbose=True)

    if args.filetype != 'live':
        try:
            c.convert()
            c.view()
        except KeyboardInterrupt:
            print('Exiting...')

if __name__ == '__main__':
    main()
