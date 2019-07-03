import os
from argparse import ArgumentParser
import model as md
from utils import create_link
from testing import test
from validation import validation


# To get arguments from commandline
def get_args():
    parser = ArgumentParser(description='cycleGAN PyTorch')
    parser.add_argument('--epochs', type=int, default=400)
    parser.add_argument('--n_channels', type=int, default=21)
    parser.add_argument('--decay_epoch', type=int, default=100)
    parser.add_argument('--batch_size', type=int, default=5)
    parser.add_argument('--lr', type=float, default=.0002)
    parser.add_argument('--load_height', type=int, default=286)
    parser.add_argument('--load_width', type=int, default=286)
    parser.add_argument('--gpu_ids', type=str, default='0')
    parser.add_argument('--crop_height', type=int, default=128)
    parser.add_argument('--crop_width', type=int, default=128)
    parser.add_argument('--lamda_img', type=int, default=1)
    parser.add_argument('--lamda_gt', type=int, default=0.05)
    parser.add_argument('--idt_coef', type=float, default=0.5)
    parser.add_argument('--omega', type=int, default=5)
    parser.add_argument('--gen_weight', type=int, default=1)
    parser.add_argument('--adversarial_weight', type=int, default=0.5)
    parser.add_argument('--discriminator_weight', type=int, default=1.0)
    parser.add_argument('--training', type=bool, default=False)
    parser.add_argument('--testing', type=bool, default=False)
    parser.add_argument('--validation', type=bool, default=False)
    parser.add_argument('--model', type=str, default='supervised_model')
    parser.add_argument('--results_dir', type=str, default='./results')
    parser.add_argument('--validation_dir', type=str, default='./val_results')
    parser.add_argument('--checkpoint_dir', type=str, default='./checkpoints/semisupervised_cycleGAN')
    parser.add_argument('--dataset',type=str,choices=['voc2012', 'cityscapes'],default='voc2012')
    parser.add_argument('--norm', type=str, default='instance', help='instance normalization or batch normalization')
    parser.add_argument('--no_dropout', action='store_true', help='no dropout for the generator')
    parser.add_argument('--ngf', type=int, default=64, help='# of gen filters in first conv layer')
    parser.add_argument('--ndf', type=int, default=64, help='# of discrim filters in first conv layer')
    parser.add_argument('--gen_net', type=str, default='resnet_9blocks')
    parser.add_argument('--dis_net', type=str, default='n_layers')
    args = parser.parse_args()
    return args


def main():
  args = get_args()
  # set gpu ids
  str_ids = args.gpu_ids.split(',')
  args.gpu_ids = []
  for str_id in str_ids:
    id = int(str_id)
    if id >= 0:
      args.gpu_ids.append(id)

  if args.training:
    if args.model == "semisupervised_cycleGAN":
      print("Training semi-supervised cycleGAN")
      model = md.semisuper_cycleGAN(args)
      model.train(args)
    if args.model == "supervised_model":
      print("Training base model")
      model = md.supervised_model(args)
      model.train(args)
  if args.testing:
      print("Testing")
      test(args)
  if args.validation:
      print("Validating")
      validation(args)


if __name__ == '__main__':
    main()
