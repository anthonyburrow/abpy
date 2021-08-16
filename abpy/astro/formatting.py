def epoch_text(epoch: float) -> str:
    epoch_text = f'{epoch:.1f}'

    if epoch >= 0:
        epoch_text = f'+{epoch_text}'

    return epoch_text
