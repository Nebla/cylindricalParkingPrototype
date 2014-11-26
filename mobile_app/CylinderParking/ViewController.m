//
//  ViewController.m
//  CylinderParking
//
//  Created by Adrian Duran on 24/11/14.
//  Copyright (c) 2014 AD. All rights reserved.
//

#import "ViewController.h"

#import "FPPopoverController.h"
#import "PlatformCollectionViewCell.h"
#import "CylinderSelectorViewController.h"

#define COLUMNS 3
#define LEVELS 5

@interface ViewController ()

@end

@implementation ViewController

- (void) viewWillAppear:(BOOL) animated
{
    [super viewWillAppear:animated];
    [cylinderButton setTitle:@"Cylinder 1" forState:UIControlStateNormal];
    
    vehicles = [[NSMutableArray alloc] init];
    
    for (int i = 0; i < COLUMNS * LEVELS; ++i) {
        NSString *patente = @"";
        NSString *imagen = @"";
        UIColor *color = [UIColor colorWithRed:150/255.0 green:150/255.0 blue:150/255.0 alpha:1];
        
        int randNum = rand() % (999 - 100) + 100; //create the random number.
        
        int randColor = rand() % (5 - 1) + 1;
        
        switch (i % 5) {
            case 0:
                patente = @"AAA";
                patente = [NSString stringWithFormat:@"%@-%d",patente,randNum];
                imagen = @"MotoSide.png";
                color = [self getColor:randColor];
                break;
            case 1:
                patente = @"BBB";
                patente = [NSString stringWithFormat:@"%@-%d",patente,randNum];
                imagen = @"CarSide.png";
                color = [self getColor:randColor];
                break;
            case 2:
                patente = @"CCC";
                patente = [NSString stringWithFormat:@"%@-%d",patente,randNum];
                imagen = @"AutoTruckSide.png";
                color = [self getColor:randColor];
                break;
            case 3:
                patente = @"DDD";
                patente = [NSString stringWithFormat:@"%@-%d",patente,randNum];
                imagen = @"TrukSide.png";
                color = [self getColor:randColor];
                break;
            case 4:
                break;
            default:
                break;
        }
        NSDictionary *dic = [[NSDictionary alloc] initWithObjectsAndKeys:patente,@"patente",imagen,@"imagen",color,@"color", nil];
        [vehicles addObject:dic];
    }
}


- (void) selectedNewCylinder:(NSInteger)cylinder {
    // Get new cylinder info
    if (cylinder < 3) {
        [cylinderButton setTitle:[NSString stringWithFormat:@"Cylinder %ld",(long)cylinder] forState:UIControlStateNormal];
    }
    else {
        [cylinderButton setTitle:@"Parking Slot" forState:UIControlStateNormal];
    }
    
}

- (IBAction)onSelectCylinderTUI:(id)sender {
    //the view controller you want to present as popover
    UIStoryboard *sb = [UIStoryboard storyboardWithName:@"Main" bundle:nil];
    CylinderSelectorViewController *controller = (CylinderSelectorViewController *)[sb instantiateViewControllerWithIdentifier:@"CylinderSelectorViewController"];
    controller.cylinder = self;
    //our popover
    FPPopoverController *popover = [[FPPopoverController alloc] initWithViewController:controller];
    
    //the popover will be presented from the okButton view
    [popover presentPopoverFromView:sender];
    
}

- (UIColor *)getColor:(NSInteger)index {
    UIColor *backgroundColor = [UIColor colorWithRed:150/255.0 green:150/255.0 blue:150/255.0 alpha:1];
    switch (index) {
        case 1:
            backgroundColor = [UIColor colorWithRed:100/255.0 green:100/255.0 blue:255/255.0 alpha:1];
            break;
        case 2:
            backgroundColor = [UIColor colorWithRed:255/255.0 green:100/255.0 blue:100/255.0 alpha:1];
            break;
        case 3:
            backgroundColor = [UIColor colorWithRed:150/255.0 green:100/255.0 blue:255/255.0 alpha:1];
            break;
        case 4:
            backgroundColor = [UIColor colorWithRed:200/255.0 green:100/255.0 blue:255/255.0 alpha:1];
            break;
        case 5:
            backgroundColor = [UIColor colorWithRed:255/255.0 green:100/255.0 blue:255/255.0 alpha:1];
            break;
        default:
            break;
    }
    
    return backgroundColor;

}

- (void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath {
    
    NSString *patente = [[vehicles objectAtIndex:indexPath.row] objectForKey:@"patente"];
    
    if ([patente length] > 0) {
        NSString *msg = [NSString stringWithFormat:@"Do you want to withdraw vehicle %@",patente];
        
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Confirmation" message:msg delegate:nil cancelButtonTitle:@"Acept" otherButtonTitles:@"Cancel", nil];
        [alert show];

    }
}


#pragma mark - UICollectionViewDataSource

- (NSInteger)collectionView:(UICollectionView *)collectionView numberOfItemsInSection:(NSInteger)section {
    return COLUMNS*LEVELS;
}

// The cell that is returned must be retrieved from a call to -dequeueReusableCellWithReuseIdentifier:forIndexPath:
- (UICollectionViewCell *)collectionView:(UICollectionView *)collectionView cellForItemAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *identifier = @"PlatformCollectionViewCell";
    
    PlatformCollectionViewCell *cell = (PlatformCollectionViewCell *)[collectionView dequeueReusableCellWithReuseIdentifier:identifier forIndexPath:indexPath];
    
    
    
    NSMutableDictionary *dict = [vehicles objectAtIndex:indexPath.row];
    
    [cell.backgroundView setBackgroundColor:[dict objectForKey:@"color"]];
    [cell.vehicleIdLabel setText:[dict objectForKey:@"patente"]];
    [cell.vehicleImage setImage:[UIImage imageNamed:[dict objectForKey:@"imagen"]]];
    
    return cell;
}


@end
