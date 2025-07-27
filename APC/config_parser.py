import argparse


def get_args_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--OPENAI_API_KEY", default="", type=str,
                        help="Enter your own API_KEY")
    parser.add_argument("--OPENAI_BASE_URL", default="", type=str,
                        help="Enter the corresponding BASE_URL")
    parser.add_argument("--model", default="", type=str,
                        help="Enter the corresponding model")
    parser.add_argument("--template", default=True, type=bool,
                        help="If True, use predefined layouts for output; if False, use predefined components for output")
    parser.add_argument("--output_dir", default='./output/', type=str,
                        help="PPT output path")
    parser.add_argument('--image', default='18', type=str,
                        help="If None, a random background image is selected. If a specific number, the specified background image is used.")
      
    args = parser.parse_args()
    return args