//
//  ViewController.h
//  CylinderParking
//
//  Created by Adrian Duran on 24/11/14.
//  Copyright (c) 2014 AD. All rights reserved.
//

#import <UIKit/UIKit.h>

@class FPPopoverController;

@interface ViewController : UIViewController <UICollectionViewDataSource, UICollectionViewDelegate, UIAlertViewDelegate, UITableViewDelegate, UITableViewDataSource> {
    NSMutableArray *vehicles;
    NSMutableArray *parkingSlot;

    __weak IBOutlet UIButton *cylinderButton;
    __weak IBOutlet UICollectionView *cylinderView;
    
    __weak IBOutlet UITableView *parkingSlotView;
    NSInteger currentCylinder;
    FPPopoverController *popover;
    
    NSInteger selectedIndex;
}

- (void) selectedNewCylinder:(NSInteger)cylinder;

@end

