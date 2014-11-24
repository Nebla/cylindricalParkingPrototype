//
//  PlatformCollectionViewCell.h
//  CylinderParking
//
//  Created by Adrian Duran on 24/11/14.
//  Copyright (c) 2014 AD. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface PlatformCollectionViewCell : UICollectionViewCell

@property (weak, nonatomic) IBOutlet UIView *backgroundView;
@property (weak, nonatomic) IBOutlet UILabel *vehicleIdLabel;
@property (weak, nonatomic) IBOutlet UIImageView *vehicleImage;

@end
