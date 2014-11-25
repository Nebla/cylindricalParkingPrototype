//
//  ViewController.m
//  CylinderParking
//
//  Created by Adrian Duran on 24/11/14.
//  Copyright (c) 2014 AD. All rights reserved.
//

#import "ViewController.h"

#import "PlatformCollectionViewCell.h"

#define COLUMNS 3
#define LEVELS 6

@interface ViewController ()

@end

@implementation ViewController

- (IBAction)onSelectCylinderTUI:(id)sender {
    
}

#pragma mark - UICollectionViewDataSource

- (NSInteger)collectionView:(UICollectionView *)collectionView numberOfItemsInSection:(NSInteger)section {
    return COLUMNS*LEVELS;
}

// The cell that is returned must be retrieved from a call to -dequeueReusableCellWithReuseIdentifier:forIndexPath:
- (UICollectionViewCell *)collectionView:(UICollectionView *)collectionView cellForItemAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *identifier = @"PlatformCollectionViewCell";
    
    PlatformCollectionViewCell *cell = (PlatformCollectionViewCell *)[collectionView dequeueReusableCellWithReuseIdentifier:identifier forIndexPath:indexPath];
    
    NSString *patente = @"";
    NSString *vehicleName = @"";
    UIColor *backGroundColor = [UIColor grayColor];
    switch (indexPath.row % 5) {
        case 0:
            patente = @"AAA-111";
            vehicleName = @"MotoSide.png";
            backGroundColor = [UIColor redColor];
            break;
        case 1:
            patente = @"BBB-222";
            vehicleName = @"CarSide.png";
            backGroundColor = [UIColor greenColor];
            break;
        case 2:
            patente = @"CCC-333";
            vehicleName = @"AutoTruckSide.png";
            backGroundColor = [UIColor blueColor];
            break;
        case 3:
            patente = @"DDD-444";
            vehicleName = @"TrukSide.png";
            backGroundColor = [UIColor purpleColor];
            break;
        case 4:
            break;
        default:
            break;
    }
    
    [cell.backgroundView setBackgroundColor:backGroundColor];
    [cell.vehicleIdLabel setText:patente];
    [cell.vehicleImage setImage:[UIImage imageNamed:vehicleName]];
    
    return cell;
}


@end
