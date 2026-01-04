import logging

logger = logging.getLogger("CopierUtils")

def calculate_lot_size(master_lot, master_equity, follower_equity, mode, config_trade):
    """
    Calculates the lot size for the follower based on the selected mode.
    
    Args:
        master_lot (float): Lot size of the master trade.
        master_equity (float): Equity of the master account.
        follower_equity (float): Equity of the follower account.
        mode (str): 'identical' or 'proportional'.
        config_trade (dict): Configuration dictionary containing 'min_lot' and 'max_lot'.
        
    Returns:
        float: The calculated lot size found to be safe and within limits.
    """
    min_lot = config_trade.get("min_lot", 0.01)
    max_lot = config_trade.get("max_lot", 10.0)
    
    final_lot = 0.0

    if mode == "identical":
        final_lot = master_lot
    elif mode == "proportional":
        if master_equity <= 0:
            logger.warning("Master equity is 0 or negative, defaulting to min_lot")
            final_lot = min_lot
        else:
            ratio = follower_equity / master_equity
            raw_lot = master_lot * ratio
            final_lot = round(raw_lot, 2) # Standard 2 decimal places for lots
    else:
        logger.warning(f"Unknown mode {mode}, defaulting to min_lot")
        final_lot = min_lot

    # Apply Caps
    if final_lot < min_lot:
        final_lot = min_lot
    if final_lot > max_lot:
        logger.warning(f"Calculated lot {final_lot} exceeds max {max_lot}, capping.")
        final_lot = max_lot
        
    return final_lot

def normalize_symbol(master_symbol):
    """
    Normalizes symbol names if needed (e.g. EURUSD.m -> EURUSD).
    For now returns as is, but placehoder for future mapping.
    """
    return master_symbol
